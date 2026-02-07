export default {
    async fetch(request) {
          const url = new URL(request.url);

      // If requesting root or any path, serve the index.html with proper content type
      if (url.pathname === '/' || url.pathname === '') {
              const response = await fetch(new Request(new URL('/index.html', url)));
              const content = await response.text();

            return new Response(content, {
                      status: 200,
                      headers: {
                                  'Content-Type': 'text/html; charset=utf-8',
                                  'Cache-Control': 'max-age=3600'
                      }
            });
      }

      // For all other requests, fetch the asset with proper content types
      const response = await fetch(request);
          const contentType = response.headers.get('content-type') || '';

      // If it's an HTML file, ensure proper content type
      if (url.pathname.endsWith('.html')) {
              return new Response(response.body, {
                        status: response.status,
                        headers: {
                                    ...Object.fromEntries(response.headers.entries()),
                                    'Content-Type': 'text/html; charset=utf-8'
                        }
              });
      }

      return response;
    }
};
