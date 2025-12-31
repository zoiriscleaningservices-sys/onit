const prompt = `
You are a professional SEO blog writer for Zoiris Cleaning Services in Sydney, Australia.

Generate ONE completely new and unique cleaning service post. Never repeat ideas.

Strictly respond with ONLY pure JSON (no markdown, no extra text):

{
  "title": "Catchy title like 'Professional End of Lease Cleaning Sydney'",
  "slug": "lowercase-hyphenated-slug",
  "content": "Full detailed description (300-500 words). Include benefits, what's covered, why choose Zoiris in Sydney, natural keywords like 'cleaning services Sydney', phone bold, etc. Use **bold** for key phrases."
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
      generationConfig: { responseMimeType: "application/json" }
    })
  }
);

if (!aiRes.ok) throw new Error("Gemini failed: " + await aiRes.text());

const aiData = await aiRes.json();
const textResponse = aiData.candidates[0].content.parts[0].text;

let blog;
try { blog = JSON.parse(textResponse); } catch (e) { throw new Error("Bad JSON from Gemini"); }

console.log("🌟 Generated:", blog.title);

// Hardcoded real public image URLs for variety (professional cleaning photos)
const profiles = [
  "https://fluxcms.com.au/wp-content/uploads/2025/06/carpet-cleaning4.jpg",
  "https://websitebydesign.com.au/wp-content/uploads/2025/07/office-cleaning12.jpg",
  "https://fluxcms.com.au/wp-content/uploads/2025/07/carpet-cleaning5-1024x726.jpg",
  "https://www.sparkleencleaning.com.au/wp-content/uploads/2022/08/Warehouse-Cleaning.jpg",
  "https://image6.slideserve.com/11960057/office-cleaning-l.jpg"
];

const galleries = [
  "https://media.istockphoto.com/id/1281015066/photo/house-mess-and-junk-declutter.jpg?s=612x612",
  "https://cdn.apartmenttherapy.info/image/upload/f_auto,q_auto:eco,c_fill,g_auto,w_1500,ar_3:2/at%2Fart%2Fdesign%2FSpecial-Projects%2F2024%2F02_BeforeAfter%2FMetadata-Images%2FAT-Before-After_Metadata-3",
  "https://media.houseandgarden.co.uk/photos/67879170ef5ba82e72c39a22/master/w_1024%2Cc_limit/DesignAndThat.Yard.CulverdenRd.ECH-36.jpg"
];

// Pick random images
const profile = profiles[Math.floor(Math.random() * profiles.length)];
const photos = [galleries[0], galleries[1], galleries[2]]; // 3 gallery photos

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
    profile: profile,
    photos: photos
  })
});

if (supabaseRes.ok) {
  console.log("🌟 SUCCESS! New post added:", blog.title, "| Profile:", profile);
} else {
  throw new Error("Supabase insert failed: " + await supabaseRes.text());
}
