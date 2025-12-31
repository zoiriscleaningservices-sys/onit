// This agent will auto-create and "publish" a full blog post every 5 minutes
// Just like you do manually in the dashboard

const prompt = `You are an expert blog writer for Zoiris Cleaning Services in Sydney, Australia.

Generate ONE completely new, unique cleaning service blog post.

Respond ONLY with pure valid JSON in this exact format:

{
  "title": "Catchy title like 'Professional Oven Cleaning Sydney - Sparkling Results Guaranteed'",
  "slug": "oven-cleaning-sydney",
  "content": "Full detailed blog post (350-500 words). Explain the service, benefits, what’s included, why choose Zoiris, mention Sydney locations, and use **bold** for key phrases like **professional cleaning** or **eco-friendly products**."
}
`;

console.log("🌟 Generating new blog post with Gemini...");

const res = await fetch(`https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${process.env.GEMINI_API_KEY}`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    contents: [{ parts: [{ text: prompt }] }],
    generationConfig: { responseMimeType: "application/json" }
  })
});

if (!res.ok) {
  const err = await res.text();
  console.error("Gemini failed:", err);
  throw new Error("AI generation failed");
}

const data = await res.json();
const jsonText = data.candidates[0].content.parts[0].text;

let post;
try {
  post = JSON.parse(jsonText);
} catch (e) {
  console.error("Bad JSON from Gemini:", jsonText);
  throw e;
}

console.log("🌟 AI created title:", post.title);

// Beautiful real cleaning images (public URLs - no upload needed)
const featuredImages = [
  "https://images.unsplash.com/photo-1581578731548-7f8c0f4d09a9?w=800",
  "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800",
  "https://images.unsplash.com/photo-1556912172-3a5f87c6c8d8?w=800",
  "https://images.unsplash.com/photo-1584622650111-993a4266b0e6?w=800",
  "https://images.unsplash.com/photo-1600565193348-f74bd86e3e1c?w=800"
];

const galleryImages = [
  "https://images.unsplash.com/photo-1558618664-3756f1d8b2a7?w=600",
  "https://images.unsplash.com/photo-1581578731548-7f8c0f4d09a9?w=600",
  "https://images.unsplash.com/photo-1556912172-3a5f87c6c8d8?w=600",
  "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600"
];

const profile = featuredImages[Math.floor(Math.random() * featuredImages.length)];
const photos = [
  galleryImages[0],
  galleryImages[1],
  galleryImages[2],
  galleryImages[3]
];

console.log("🌟 Adding images to post");

// Publish to Supabase - exactly like your dashboard does
const supabaseRes = await fetch(`${process.env.SUPABASE_URL}/rest/v1/services`, {
  method: "POST",
  headers: {
    "apikey": process.env.SUPABASE_SERVICE_KEY,
    "Authorization": `Bearer ${process.env.SUPABASE_SERVICE_KEY}`,
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
  },
  body: JSON.stringify({
    name: post.title,
    slug: post.slug,
    description: post.content,
    profile: profile,
    photos: photos,
    created_at: new Date().toISOString()
  })
});

if (supabaseRes.ok) {
  console.log("🎉 SUCCESS! New blog post published automatically!");
  console.log("Title:", post.title);
  console.log("Live on dashboard: https://www.zoiriscleaningservices.com/dashboard.html");
  console.log("View post live: https://www.zoiriscleaningservices.com/blog/" + post.slug);
} else {
  const errorText = await supabaseRes.text();
  console.error("Supabase failed:", errorText);
  throw new Error("Failed to publish post");
}
