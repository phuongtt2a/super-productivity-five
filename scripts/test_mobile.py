"""Local visual regression and mobile interaction checks (requires Playwright + Chromium)."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'plugin/index.html').read_text(encoding='utf8')
OUT=ROOT/'docs/screenshots'
SIZES=[(320,568),(360,640),(375,667),(390,844),(430,932),(540,720),(600,760),(667,375),(844,390)]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-gpu'])
 for w,h in SIZES:
  context=b.new_context(viewport={'width':w,'height':h},color_scheme='dark',device_scale_factor=1,reduced_motion='reduce',has_touch=w<768)
  page=context.new_page()
  page.set_content(HTML,wait_until='domcontentloaded')
  page.wait_for_selector('.focus-row')
  # Exercise the actual host font variable and Vietnamese glyphs/wrapping.
  page.evaluate("""() => {
    const root=document.documentElement;
    root.classList.add('sp-host','sp-dark');
    root.style.setProperty('--text-color','#f3f3f0');
    root.style.setProperty('--text-color-muted','#b1bfc6');
    root.style.setProperty('--bg','#192631');
    root.style.setProperty('--bg-lighter','#293945');
    root.style.setProperty('--card-bg','#26333b');
  }""")
  page.add_style_tag(content="""html::before{content:'';pointer-events:none;position:fixed;inset:0;z-index:-1;background:linear-gradient(140deg,rgba(76,138,108,.24),transparent 60%),var(--bg)}""")
  assert page.evaluate("getComputedStyle(document.body).backgroundColor")=="rgba(0, 0, 0, 0)"
  assert page.evaluate("getComputedStyle(document.documentElement).backgroundColor")=="rgba(0, 0, 0, 0)"
  assert page.evaluate("Math.abs(document.querySelector('.app').getBoundingClientRect().width-Math.min(innerWidth,1220))<1")
  page.evaluate("""() => {
    document.documentElement.style.setProperty('--font-primary-stack', '"Segoe UI",Arial,sans-serif');
    const vietnamese = [
      'Hoàn thiện giao diện quản lý công việc hôm nay',
      'Kiểm tra tính tương thích trên điện thoại',
      'Cập nhật báo cáo doanh thu tháng này',
      'Sửa lỗi đăng nhập người dùng',
      'Chuẩn bị cuộc họp chiều nay',
      'Đánh giá yêu cầu từ khách hàng'
    ];
    state.tasks.forEach((task, i) => { task.title = vietnamese[i % vietnamese.length]; });
    state.projects.forEach((project,i)=>{project.title = i === 0 ? 'Dự án cá nhân' : 'Công việc';});
    render();
  }""")
  assert 'Segoe UI' in page.locator('.focus-title').first.evaluate('(el)=>getComputedStyle(el).fontFamily'),(w,h,'host font was not applied')
  assert page.locator('.focus-row').count()==5,(w,h)
  geo=page.evaluate('''()=>({width:document.documentElement.scrollWidth,screen:innerWidth,
  list:document.querySelector('#focus-list').getBoundingClientRect().bottom,
  footer:document.querySelector('.footline').getBoundingClientRect().bottom,
  circles:[...document.querySelectorAll('.complete-button')].map(e=>{let r=e.getBoundingClientRect();return [r.width,r.height]})})''')
  assert geo['width']<=w+1,(w,h,geo)
  assert geo['footer']<=h+1,(w,h,geo)
  assert all(abs(a-b)<.5 for a,b in geo['circles']),(w,h,geo)
  # Titles must remain inside their allotted row; long Vietnamese text can
  # occupy two lines, but must never overlap the following priority.
  title_geometry=page.evaluate("""() => [...document.querySelectorAll('.focus-row')].map(row => {
    const title=row.querySelector('.focus-title');
    if (!title) return null;
    const a=title.getBoundingClientRect(),b=row.getBoundingClientRect();
    return {top:a.top,bottom:a.bottom,rowTop:b.top,rowBottom:b.bottom};
  })""")
  assert all(not t or (t['top']>=t['rowTop']-1 and t['bottom']<=t['rowBottom']+1) for t in title_geometry),(w,h,title_geometry)
  page.locator('#manage-button').click()
  assert page.evaluate('document.documentElement.scrollWidth')<=w+1,(w,h,'manage horizontal scroll')
  page.locator('#new-task-button').click()
  if w<=790 or h<=560:
   form=page.locator('#create-form')
   assert form.evaluate('(el)=>getComputedStyle(el).overflowY')=='auto',(w,h,'form not scrollable')
   page.locator('#submit-create').scroll_into_view_if_needed(timeout=1500)
   assert page.locator('#submit-create').is_visible(),(w,h,'create submit inaccessible')
  page.locator('#cancel-create').click()
  if w<=790:
   page.locator('#tab-selected').click()
   queue=page.locator('#selected-queue')
   assert queue.evaluate('(el)=>getComputedStyle(el).overflowY')=='auto',(w,h,'queue not scrollable')
   page.locator('.queue-row').last.scroll_into_view_if_needed(timeout=1500)
   assert page.locator('.queue-row').last.is_visible(),(w,h,'last queue item inaccessible')
  if (w,h)==(390,844):
   page.locator('#back-button').click()
   # Each image uses actual plugin rendering with browser sample data.
   for key,setup in [('focus-phone',None),('arrange-phone','#manage-button')]:
    if setup:page.locator(setup).click()
    out=OUT/f'{key}-v1.0.5.webp';
    # JPEG is used as the Playwright intermediate to avoid transparency
    # getting composited unexpectedly by the WebP converter.
    page.screenshot(path=str(out),type='jpeg',quality=88)
    Image.open(out).convert('RGB').save(out,format='WEBP',quality=86)
  if (w,h)==(320,568):
   page.locator('#back-button').click()
   page.locator('#manage-button').click()
   page.locator('#tab-browse').click()
   page.locator('#new-task-button').click()
   page.locator('#submit-create').scroll_into_view_if_needed()
   out=OUT/'create-phone-v1.0.5.webp';page.screenshot(path=str(out),type='jpeg',quality=88)
   Image.open(out).convert('RGB').save(out,format='WEBP',quality=86)
  print(f'PASS {w}x{h}: 5 visible focus tasks, no horizontal overflow, editor and priority queue reachable')
  context.close()
 b.close()
