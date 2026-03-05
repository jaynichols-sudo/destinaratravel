export async function onRequestPost(context) {
  const { request, env } = context;

  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
  };

  try {
    const body = await request.json();
    const { destination, duration, travelers, style, budget } = body;

    if (!destination) {
      return new Response(JSON.stringify({ error: 'Destination is required' }), {
        status: 400, headers: corsHeaders,
      });
    }

    const prompt = `You are a travel budget expert. Generate a detailed travel budget estimate for the following trip:

Destination: ${destination}
Duration: ${duration || '7 days'}
Number of travelers: ${travelers || 1}
Travel style: ${style || 'moderate'}
Budget preference: ${budget || 'moderate'}

Respond with ONLY a valid JSON object in this exact format (no markdown, no explanation):
{
  "destination": "Full destination name",
  "duration": "X days",
  "travelers": N,
  "style": "travel style",
  "summary": "One sentence overview of this trip budget",
  "categories": {
    "flights": { "low": 000, "high": 000, "notes": "Brief note about flights" },
    "accommodation": { "low": 000, "high": 000, "notes": "Brief note about accommodation" },
    "food": { "low": 000, "high": 000, "notes": "Brief note about food and dining" },
    "activities": { "low": 000, "high": 000, "notes": "Brief note about activities" },
    "transport": { "low": 000, "high": 000, "notes": "Brief note about local transport" },
    "misc": { "low": 000, "high": 000, "notes": "Visa, insurance, tips, souvenirs" }
  },
  "totalLow": 0000,
  "totalHigh": 0000,
  "tips": ["Practical tip 1", "Practical tip 2", "Practical tip 3"],
  "bestTime": "Best time of year to visit",
  "currency": "Local currency name and approximate exchange rate"
}`;

    const apiKey = env.ANTHROPIC_API_KEY;
    if (!apiKey) {
      return new Response(JSON.stringify({ error: 'API key not configured', debug: 'ANTHROPIC_API_KEY env var is missing' }), {
        status: 500, headers: corsHeaders,
      });
    }

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-3-5-haiku-20241022',
        max_tokens: 1024,
        messages: [{ role: 'user', content: prompt }],
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      return new Response(JSON.stringify({ error: 'Anthropic API error', status: response.status, detail: errorText }), {
        status: 500, headers: corsHeaders,
      });
    }

    const data = await response.json();
    const text = data.content[0].text.trim();

    let estimate;
    try {
      estimate = JSON.parse(text);
    } catch (e) {
      const match = text.match(/```(?:json)?\n?([sS]*?)```/);
      if (match) {
        estimate = JSON.parse(match[1]);
      } else {
        return new Response(JSON.stringify({ error: 'Parse error', rawText: text.substring(0, 500) }), {
          status: 500, headers: corsHeaders,
        });
      }
    }

    return new Response(JSON.stringify(estimate), {
      status: 200, headers: corsHeaders,
    });

  } catch (err) {
    return new Response(JSON.stringify({ error: 'Internal server error', detail: err.message }), {
      status: 500, headers: corsHeaders,
    });
  }
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}
