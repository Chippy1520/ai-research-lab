"""Optional browser regression check: python scripts/verify_mindmap_ui.py.

Requires Playwright + Chromium in the invoking environment. Serves only site/
locally and blocks external requests; never accesses the private companion.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from tempfile import gettempdir

from playwright.sync_api import sync_playwright, expect


def main():
    root = Path(__file__).resolve().parents[1]
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(root / 'site')))
    Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    screenshots = Path(gettempdir()) / 'mindmap-atelier'
    screenshots.mkdir(exist_ok=True)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=[f'--explicitly-allowed-ports={server.server_port}'])
            page = browser.new_page(viewport={'width': 1440, 'height': 1000})
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.route('**/*', lambda route: route.continue_() if route.request.url.startswith(base + '/') else route.abort())
            page.goto(base + '/mindmap.html')
            page.wait_for_selector('.mm-node.domain')
            points = page.locator('.mm-node.domain').evaluate_all('(nodes) => nodes.map(n => {const t=n.transform.baseVal.getItem(0).matrix;return [t.e,t.f]})')
            assert len(points) == 6
            assert sum(x < 650 for x, _ in points) >= 2, points
            assert sum(x > 650 for x, _ in points) >= 2, points
            assert sum(y < 650 for _, y in points) >= 2, points
            assert sum(y > 650 for _, y in points) >= 2, points
            assert page.locator('.mm-edge.cross').count() == 0
            assert page.locator('.mm-private-link').count() == 0
            page.screenshot(path=str(screenshots / 'desktop.png'))

            page.goto(base + '/mindmap.html#node=gen15')
            page.wait_for_selector('.mm-edge.cross')
            assert page.locator('.mm-edge.cross[data-to="generalist-ai"]').count() == 1
            related = page.locator('.mm-node[data-id="generalist-ai"]')
            assert 'ghost' not in (related.get_attribute('class') or '')
            related.click()
            assert page.locator('#mm-panel-body h2').inner_text() == 'Generalist AI'
            assert page.locator('#mm-crumb').inner_text().endswith('Foundation-model labs')
            page.locator('#mm-top').click()
            assert page.locator('.mm-edge.cross').count() == 0
            assert page.locator('.mm-node.domain').evaluate_all('(nodes) => nodes.map(n => {const t=n.transform.baseVal.getItem(0).matrix;return [t.e,t.f]})') == points

            page.goto(base + '/mindmap.html?career=1#node=openvla')
            page.wait_for_selector('.mm-person-card')
            assert page.locator('.mm-linkedin').count() >= 3
            assert page.locator('.mm-person-card').first.locator('h4').inner_text() == 'Moo Jin Kim'
            assert page.locator('.mm-private-link').get_attribute('href') == 'http://127.0.0.1:8767/#node=openvla'
            page.locator('.mm-provenance summary').first.click()
            assert page.locator('.mm-provenance').first.get_attribute('open') is not None
            page.locator('.mm-person-card').first.scroll_into_view_if_needed()
            page.screenshot(path=str(screenshots / 'desktop-profile.png'))

            for width, height in [(390, 844), (360, 740)]:
                mobile = browser.new_context(viewport={'width': width, 'height': height}, is_mobile=True, has_touch=True)
                phone = mobile.new_page()
                phone.on('pageerror', lambda error: errors.append(str(error)))
                phone.route('**/*', lambda route: route.continue_() if route.request.url.startswith(base + '/') else route.abort())
                phone.goto(base + '/mindmap.html')
                phone.wait_for_selector('.mm-node.domain')
                phone.evaluate('document.fonts.ready')
                assert phone.evaluate('document.documentElement.scrollWidth <= innerWidth')
                assert phone.locator('#mm-svg').bounding_box()['height'] > height * .7
                def check_labels():
                    assert phone.locator('.mm-node:not(.ghost) text').evaluate_all('''nodes => nodes.every(n => {
                      const b=n.getBoundingClientRect(), s=document.querySelector('#mm-svg').getBoundingClientRect();
                      return b.left >= s.left && b.right <= s.right && b.top >= s.top && b.bottom <= s.bottom;
                    })'''), 'A live label is clipped'
                check_labels()
                phone.screenshot(path=str(screenshots / f'mobile-{width}.png'))
                transform = lambda: phone.locator('#mm-svg > g').get_attribute('transform')
                before = transform()
                phone.locator('#mm-zoom-in').tap()
                assert transform() != before
                phone.locator('#mm-fit').tap()
                assert transform() == before
                # Real browser touch events, not synthetic JS pointer dispatch.
                cdp = mobile.new_cdp_session(phone)
                y = int(height * .5)
                cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': 120, 'y': y}, {'x': 220, 'y': y}]})
                cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': 80, 'y': y - 20}, {'x': 260, 'y': y + 20}]})
                cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
                assert transform() != before, 'Pinch must change camera'
                phone.locator('#mm-fit').tap()
                cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': 70, 'y': y}]})
                cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': 105, 'y': y + 30}]})
                cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
                assert transform() != before, 'Pan must change camera'
                phone.goto(base + '/mindmap.html#node=openvla')
                phone.wait_for_selector('.mm-person-card', state='attached')
                check_labels()
                phone.screenshot(path=str(screenshots / f'mobile-branch-{width}.png'))
                toggle = phone.locator('#mm-sheet-toggle')
                toggle.click()
                expect(toggle).to_have_attribute('aria-expanded', 'true')
                card = phone.locator('.mm-person-card').first
                card.scroll_into_view_if_needed()
                assert card.bounding_box()['width'] <= width - 30
                phone.screenshot(path=str(screenshots / f'mobile-profile-{width}.png'))
                toggle.click()
                expect(toggle).to_have_attribute('aria-expanded', 'false')
                assert not phone.locator('#mm-panel-body').is_visible()
                mobile.close()
            assert not errors, errors
            browser.close()
            print('PASS: 360-degree branches, semantic links, cross-branch click, home reset, LinkedIn cards, provenance, private opt-in, 390/360px label fit, zoom/fit, real touch pinch/pan, accessible sheet; no JS errors.')
            print(f'Screenshots: {screenshots.resolve()}')
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    main()
