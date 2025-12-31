import fetch from "node-fetch";

const TOPICS = [
  "House Cleaning Tips for Mobile AL Homes",
  "Deep Cleaning Services in Mobile Alabama",
  "Move Out Cleaning Checklist in Mobile AL",
  "Office Cleaning Services for Mobile Businesses"
];

const topic = TOPICS[Math.floor(Math.random() * TOPICS.length)];

const prompt = `
Write a long-form SEO blog post for Zoiris Cleaning Services in Mobile Alabama.

Topic: ${topic}

Business Info:
Company: Zoiris Cleaning Services
Phone: (251) 930-8621
Email: zoiriscleaningservices@gmail.com
Location: Mobile, AL

SEO Rules:
- Minimum 900 words
- Strong local SEO
- Use headings
- End with call-to-action

Return JSON ONLY:
{
  "title":"",
  "slug":"",
  "content":""
}
`;

const geminiRes = await fetch(
  `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${process.env.GEMINI_API_KEY}`,
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }]
    })
  }
);

const geminiData = await geminiRes.json();
const blog = JSON.parse(geminiData.candidates[0].content.parts[0].text);

// FREE image (Pexels)
const imageUrl = "https://images.pexels.com/photos/4239091/pexels-photo-4239091.jpeg";

await fetch(`${process.env.SUPABASE_URL}/rest/v1/services`, {
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
    profile: imageUrl,
    photos: [imageUrl]
  })
});

console.log("✅ Blog posted automatically");
