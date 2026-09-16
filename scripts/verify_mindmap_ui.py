"""Optional browser regression check: python scripts/verify_mindmap_ui.py.

Requires Playwright + Chromium in the invoking environment. Serves only site/
locally and blocks external requests; never accesses the private companion.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright


def main():
    root = Path(__file__).resolve().parents[1]
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(root / 'site')))
    Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
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

            page.set_viewport_size({'width': 390, 'height': 844})
            page.goto(base + '/mindmap.html#node=openvla')
            page.wait_for_selector('.mm-person-card')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            card = page.locator('.mm-person-card').first
            card.scroll_into_view_if_needed()
            assert card.bounding_box()['width'] <= 390
            assert not errors, errors
            browser.close()
            print('PASS: 360-degree branches, semantic links, cross-branch click, home reset, LinkedIn cards, provenance, private opt-in, mobile fit; no JS errors.')
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    main()
