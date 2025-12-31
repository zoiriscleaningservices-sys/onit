console.log("🌟 Prompt sent to Gemini:", prompt);

const aiRes = await fetch(
  `https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${process.env.GEMINI_API_KEY}`,
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: {
        responseMimeType: "application/json"  // Forces pure JSON output (no markdown)
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

// Parse the JSON string returned by Gemini
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
    // Change to return=representation if you want the inserted row back
    Prefer: "return=minimal"
  },
  body: JSON.stringify({
    name: blog.title,
    slug: blog.slug,
    description: blog.content,  // assuming this matches your column name
    profile: "https://images.pexels.com/photos/4239091/pexels-photo-4239091.jpeg",
    photos: ["https://images.pexels.com/photos/4239091/pexels-photo-4239091.jpeg"]
  })
});

console.log("🌟 Supabase response status:", supabaseRes.status);

if (!supabaseRes.ok) {
  const errorText = await supabaseRes.text();
  console.error("🌟 Supabase error:", errorText);
} else {
  console.log("🌟 Successfully inserted into Supabase!");
}
