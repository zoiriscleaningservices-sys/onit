// Define the prompt — this tells Gemini what kind of blog post to generate
const prompt = `
You are an expert blog writer for a cleaning services company called Zoiris Cleaning Services.

Generate ONE new unique service offering in strict JSON format (no markdown, no explanations).

Requirements:
- Make it sound professional and appealing
- Use a different service idea each time (never repeat)
- Include location: Sydney, Australia

Respond ONLY with valid JSON in this exact structure:
{
  "title": "Short catchy service title (e.g. End of Lease Cleaning Sydney)",
  "slug": "lowercase-hyphenated-version-of-title (e.g. end-of-lease-cleaning-sydney)",
  "content": "A detailed description of the service (200-400 words), explaining benefits, what’s included, and why customers should choose Zoiris."
}

Do not include any backticks, ```json, or extra text.
`;

// Now log and send to Gemini
console.log("🌟 Prompt sent to Gemini:", prompt);

const aiRes = await fetch(
  `https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${process.env.GEMINI_API_KEY}`,
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: {
        responseMimeType: "application/json"  // Forces clean JSON output
      }
    })
  }
);

if (!aiRes.ok) {
  const errorText = await aiRes.text();
  console.error("🌟 Gemini error response:", aiRes.status, errorText);
  throw new Error(`Gemini API error: ${aiRes.status}`);
}

const aiData = await aiRes.json();
console.log("🌟 Parsed AI JSON:", aiData);

if (!aiData.candidates || aiData.candidates.length === 0) {
  throw new Error("No candidates returned from Gemini");
}

const textResponse = aiData.candidates[0].content.parts[0].text;
console.log("🌟 Raw Gemini text:", textResponse);

let blog;
try {
  blog = JSON.parse(textResponse);
} catch (parseError) {
  console.error("Failed to parse Gemini response as JSON:", textResponse);
  throw parseError;
}

console.log("🌟 Blog object:", blog);

const supabaseRes = await fetch(`${process.env.SUPABASE_URL}/rest/v1/services`, {
  method: "POST",
  headers: {
    apikey: process.env.SUPABASE_SERVICE_KEY,
    Authorization: `Bearer ${process.env.SUPABASE_SERVICE_KEY}`,
    "Content-Type": "application/json",
    Prefer: "return=minimal"
  },
  body: JSON.stringify({
    name: blog.title,
    slug: blog.slug,
    description: blog.content,
    profile: "https://images.pexels.com/photos/4239091/pexels-photo-4239091.jpeg",
    photos: ["https://images.pexels.com/photos/4239091/pexels-photo-4239091.jpeg"]
  })
});

console.log("🌟 Supabase response status:", supabaseRes.status);

if (!supabaseRes.ok) {
  const errorText = await supabaseRes.text();
  console.error("🌟 Supabase error:", errorText);
  throw new Error("Failed to insert into Supabase");
} else {
  console.log("🌟 Successfully inserted new service into Supabase!");
}
