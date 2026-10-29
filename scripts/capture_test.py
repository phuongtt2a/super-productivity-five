from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'plugin/index.html').read_text(encoding='utf-8')
DOCS=ROOT/'docs/screenshots'
DOCS.mkdir(parents=True,exist_ok=True)

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
    for theme,width,height,arrange in [
        ('dark',1440,840,False),('dark',1440,900,True),
        ('light',1440,840,False),('light',1440,900,True),
        ('dark',390,780,False)]:
        context=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1,color_scheme=theme,reduced_motion='reduce')
        page=context.new_page()
        page.set_content(HTML,wait_until='domcontentloaded')
        page.wait_for_selector('[data-focus-id]',timeout=4000)
        page.evaluate('''(theme)=>{
            document.documentElement.classList.add('sp-host', theme==='dark'?'sp-dark':'sp-light');
            document.documentElement.style.setProperty('--text-color',theme==='dark'?'#f3f3f0':'#17241c');
            document.documentElement.style.setProperty('--text-color-muted',theme==='dark'?'#b1bfc6':'#556458');
            document.documentElement.style.setProperty('--bg',theme==='dark'?'#192631':'#eaf2eb');
            document.documentElement.style.setProperty('--bg-lighter',theme==='dark'?'#293945':'#f7faf3');
            document.documentElement.style.setProperty('--card-bg',theme==='dark'?'#26333b':'#eef4eb');
        }''',theme)
        # Reproduce host-provided default sizing rules; our small completion buttons
        # must remain square even when the host gives buttons a min-width & padding.
        page.add_style_tag(content='''
          button { min-width:65px; min-height:40px; padding:10px 15px; }
          html::before { content:'';pointer-events:none;position:fixed;inset:0;z-index:-1;
            background:linear-gradient(140deg,rgba(67,123,99,.25),transparent 48%),
                       linear-gradient(10deg,rgba(55,87,131,.18),transparent 56%),
                       var(--bg); }
        ''')
        page.wait_for_timeout(120)
        dims=page.locator('.complete-button').evaluate_all('els=>els.map(e=>({w:e.getBoundingClientRect().width,h:e.getBoundingClientRect().height}))')
        assert len(dims)==5,(theme,width,dims)
        assert all(abs(d['w']-d['h'])<.4 for d in dims),(theme,width,dims)
        assert all(abs(dims[i]['w']-dims[i+1]['w'])>=1 for i in range(4)),(theme,width,dims)
        assert page.locator('#focus-heading').inner_text()=='Less, but meaningful.'
        if arrange:
            page.locator('#manage-button').click()
            page.wait_for_selector('.queue-row')
        label='focus' if not arrange else 'arrange'
        suffix='phone' if width<500 else theme
        out=DOCS/f'{label}-{suffix}-v1.0.3.webp'
        png=DOCS/f'{label}-{suffix}-v1.0.3.png'
        page.screenshot(path=str(png),animations='disabled')
        Image.open(png).convert('RGB').save(out,format='WEBP',quality=84,method=6)
        png.unlink()
        print(theme,width,'arrange' if arrange else 'focus','circles',dims,'screenshot',out.name)
        context.close()
    browser.close()
