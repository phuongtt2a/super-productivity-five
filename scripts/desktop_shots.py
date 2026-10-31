"""Produce release screenshots with host font and Vietnamese example tasks."""
from pathlib import Path
from io import BytesIO
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'plugin/index.html').read_text(encoding='utf8')
OUT=ROOT/'docs/screenshots'
VIET='''() => {
 document.documentElement.style.setProperty('--font-primary-stack','"Segoe UI",Arial,sans-serif');
 const names=['Hoàn thiện giao diện quản lý công việc hôm nay',
 'Kiểm tra tính tương thích trên điện thoại',
 'Cập nhật báo cáo doanh thu tháng này',
 'Sửa lỗi đăng nhập người dùng',
 'Chuẩn bị cuộc họp chiều nay',
 'Đánh giá yêu cầu từ khách hàng'];
 state.tasks.forEach((t,i)=>t.title=names[i%names.length]);
 state.projects.forEach((p,i)=>p.title=i===0?'Dự án cá nhân':'Công việc');render();
}'''
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-gpu'])
 for mode in ('dark','light'):
  context=browser.new_context(viewport={'width':1365,'height':830},color_scheme=mode,device_scale_factor=1,reduced_motion='reduce')
  page=context.new_page();page.set_content(HTML,wait_until='domcontentloaded');page.wait_for_selector('.focus-row')
  page.evaluate("""(mode) => {
    const root=document.documentElement;
    root.classList.add('sp-host',mode==='dark'?'sp-dark':'sp-light');
    root.style.setProperty('--font-primary-stack','"Segoe UI", Arial, sans-serif');
    root.style.setProperty('--text-color',mode==='dark'?'#f3f3f0':'#17241c');
    root.style.setProperty('--text-color-muted',mode==='dark'?'#b1bfc6':'#556458');
    root.style.setProperty('--bg',mode==='dark'?'#192631':'#eaf2eb');
    root.style.setProperty('--bg-lighter',mode==='dark'?'#293945':'#f7faf3');
    root.style.setProperty('--card-bg',mode==='dark'?'#26333b':'#eef4eb');
  }""",mode)
  page.add_style_tag(content="""
    html::before{content:'';pointer-events:none;position:fixed;inset:0;z-index:-1;
      background:linear-gradient(135deg,rgba(89,143,107,.22),transparent 56%),
                 linear-gradient(12deg,rgba(117,154,198,.16),transparent 70%),var(--bg);}
  """)
  assert page.evaluate("getComputedStyle(document.body).backgroundColor")=="rgba(0, 0, 0, 0)"
  page.evaluate(VIET)
  layout=page.evaluate("""() => {
    const app=document.querySelector('.app'),focus=document.querySelector('.focus-view');
    const style=getComputedStyle(app);
    return {appWidth:app.getBoundingClientRect().width,
      innerWidth:app.getBoundingClientRect().width-parseFloat(style.paddingLeft)-parseFloat(style.paddingRight),
      focusWidth:focus.getBoundingClientRect().width,
      rootBg:getComputedStyle(document.documentElement).backgroundColor,
      bodyBg:getComputedStyle(document.body).backgroundColor,
      font:getComputedStyle(document.querySelector('.focus-title')).fontFamily};
  }""")
  assert abs(layout['appWidth']-1220)<1,(mode,layout,'shared page width')
  assert abs(layout['focusWidth']-layout['innerWidth'])<1,(mode,layout,'focus content aligned with shell')
  assert layout['rootBg']=='rgba(0, 0, 0, 0)',(mode,layout,'root transparency')
  assert layout['bodyBg']=='rgba(0, 0, 0, 0)',(mode,layout,'body transparency')
  assert 'Segoe UI' in layout['font'],(mode,layout,'host font')
  for screen in ('focus','arrange'):
   if screen=='arrange':page.locator('#manage-button').click()
   shot=page.screenshot(type='png',full_page=False)
   path=OUT/f'{screen}-{mode}-v1.0.5.webp'
   Image.open(BytesIO(shot)).convert('RGB').save(path,format='WEBP',quality=85,method=6)
   print(path.name, path.stat().st_size)
  context.close()
 browser.close()
