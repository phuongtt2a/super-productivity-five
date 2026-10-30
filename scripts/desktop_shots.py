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
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 for mode in ('dark','light'):
  context=browser.new_context(viewport={'width':1365,'height':830},color_scheme=mode,device_scale_factor=1,reduced_motion='reduce')
  page=context.new_page();page.set_content(HTML,wait_until='domcontentloaded');page.wait_for_selector('.focus-row')
  page.evaluate(VIET)
  for screen in ('focus','arrange'):
   if screen=='arrange':page.locator('#manage-button').click()
   shot=page.screenshot(type='png',full_page=False)
   path=OUT/f'{screen}-{mode}-v1.0.5.webp'
   Image.open(BytesIO(shot)).convert('RGB').save(path,format='WEBP',quality=85,method=6)
   print(path.name, path.stat().st_size)
  context.close()
 browser.close()
