"""Visual regression for narrow viewport title, project, due-date and divider collisions.

Requires Playwright and Chromium. Run: python scripts/test_focus_dividers.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'plugin/index.html').read_text(encoding='utf8')
SIZES = [(320,480),(320,568),(360,640),(375,667),(390,844),(430,932),(667,375),(844,390)]
SAMPLE = '''() => {
  document.documentElement.style.setProperty('--font-primary-stack', '"Segoe UI", Arial, sans-serif');
  state.projects = [
    {id:'p',title:'Dự án quản lý và điều hành công việc hành chính trong ngày dài'},
    {id:'q',title:'Quản lý hệ thống tài chính dự án'}
  ];
  const names = [
    'Kiểm tra giao diện trên điện thoại với văn bản khá dài và nhiều thông tin cần xử lý',
    'Hoàn thiện các tính năng dashboard và kết nối API',
    'Đối soát các thông tin giao dịch và chuẩn bị báo cáo cho đối tác',
    'Thảo luận kế hoạch phát triển quý tiếp theo',
    'Chuẩn bị nội dung và kiểm tra trạng thái của khách hàng'
  ];
  state.tasks = names.map((title,i)=>({id:'t'+i,title,projectId:i%2?'q':'p',dueDay:'2026-10-29',isDone:false,timeSpent:0}));
  state.saved.days[state.today] = state.tasks.map(t=>t.id);
  renderFocus();
}'''

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
    for w,h in SIZES:
        context = browser.new_context(viewport={'width':w,'height':h},color_scheme='dark',reduced_motion='reduce')
        page = context.new_page()
        page.set_content(HTML)
        page.wait_for_selector('.focus-row')
        page.evaluate(SAMPLE)
        rows = page.evaluate('''() => [...document.querySelectorAll('.focus-row')].map(row=>{
          const meta=row.querySelector('.focus-meta');
          const title=row.querySelector('.focus-title');
          const project=meta.querySelector('span');
          const circle=row.querySelector('.complete-button');
          const r=row.getBoundingClientRect(), m=meta.getBoundingClientRect(), t=title.getBoundingClientRect(), c=circle.getBoundingClientRect();
          return {rowBottom:r.bottom,metaBottom:m.bottom,titleBottom:t.bottom,circleWidth:c.width,circleHeight:c.height,
            metaHeight:m.height,projectText:project.textContent,projectWidth:project.getBoundingClientRect().width,
            metaText:meta.textContent};
        })''')
        assert len(rows)==5,(w,h,rows)
        for n,row in enumerate(rows,1):
            assert row['metaBottom'] <= row['rowBottom'] - 1.5, (w,h,n,row)
            assert row['titleBottom'] <= row['rowBottom'] - 1.5, (w,h,n,row)
            assert abs(row['circleWidth']-row['circleHeight']) < .5,(w,h,n,row)
            assert row['metaHeight']<=18,(w,h,n,row)
            assert 'Oct' in row['metaText'],(w,h,n,row)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'),(w,h,'horizontal overflow')
        assert page.locator('.footline').bounding_box()['y']+page.locator('.footline').bounding_box()['height']<=h+1,(w,h,'footer off screen')
        print(f'PASS {w}x{h}: all 5 rows and their one-line metadata clear every divider')
        context.close()
    browser.close()
