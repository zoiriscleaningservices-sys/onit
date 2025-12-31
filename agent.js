const prompt = `
You are an expert blog writer for Zoiris Cleaning Services, a professional cleaning company in Sydney, Australia.

Generate ONE unique new cleaning service offering. Make it fresh and different every time.

Respond ONLY with pure valid JSON in this exact format (no markdown, no extra text, no explanations):

{
  "title": "Catchy service title (e.g. Deep Kitchen Cleaning Sydney)",
  "slug": "lowercase-with-hyphens (e.g. deep-kitchen-cleaning-sydney)",
  "content": "Detailed description of the service (250-400 words). Explain what's included, benefits, and why choose Zoiris Cleaning Services in Sydney."
}
`;

console.log("🌟 Prompt sent to Gemini:", prompt);

const aiRes = await fetch(
  `https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${process.env.GEMINI_API_KEY}`,
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: {
        responseMimeType: "application/json"
      }
    })
  }
);

if (!aiRes.ok) {
  const errorText = await aiRes.text();
  console.error("🌟 Gemini error:", aiRes.status, errorText);
  throw new Error("Gemini API failed");
}

const aiData = await aiRes.json();

if (!aiData.candidates?.[0]) {
  throw new Error("No response from Gemini");
}

const textResponse = aiData.candidates[0].content.parts[0].text;
let blog;

try {
  blog = JSON.parse(textResponse);
} catch (e) {
  console.error("🌟 Failed to parse JSON:", textResponse);
  throw e;
}

console.log("🌟 Generated blog:", blog);

const supabaseRes = await fetch(`${process.env.SUPABASE_URL}/rest/v1/services`, {
  method: "POST",
  headers: {
    "apikey": process.env.SUPABASE_SERVICE_KEY,
    "Authorization": `Bearer ${process.env.SUPABASE_SERVICE_KEY}`,
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
  },
  body: JSON.stringify({
    name: blog.title,
    slug: blog.slug,
    description: blog.content,
    profile: "https://images.pexels.com/photos/4239091/pexels-photo-4239091.jpeg",
    photos: ["https://images.pexels.com/photos/4239091/pexels-photo-4239091.jpeg"]
  })
});

if (supabaseRes.ok) {
  console.log("🌟 SUCCESS! New service posted to Supabase:", blog.title);
} else {
  const err = await supabaseRes.text();
  console.error("🌟 Supabase error:", supabaseRes.status, err);
  throw new Error("Failed to save to Supabase");
}
