// Prompt for unique Mobile, AL cleaning services
const prompt = `
You are an expert SEO writer for Zoiris Cleaning Services in Mobile, Alabama, USA.

Generate ONE brand new, unique cleaning service post. Never repeat previous ideas.

Respond ONLY with pure JSON (no markdown, no extra text):

{
  "title": "Professional and catchy title (e.g. Expert Carpet Steam Cleaning Mobile AL)",
  "slug": "lowercase-with-hyphens (e.g. expert-carpet-steam-cleaning-mobile-al)",
  "content": "Detailed 300-500 word description. Cover what's included, benefits, why choose Zoiris in Mobile, include keywords naturally. Use **bold** for key terms."
}
`;

console.log("🌟 Sending prompt to Gemini...");

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

if (!aiRes.ok) {
  const err = await aiRes.text();
  console.error("Gemini error:", err);
  throw new Error("Gemini failed");
}

const aiData = await aiRes.json();
const textResponse = aiData.candidates[0].content.parts[0].text;

let blog;
try {
  blog = JSON.parse(textResponse);
} catch (e) {
  console.error("Invalid JSON:", textResponse);
  throw e;
}

console.log("🌟 Generated post:", blog.title);

// Real professional cleaning images (public URLs)
const profileImages = [
  "https://callthecleaners.com.au/wp-content/uploads/2025/12/DIY-vs-Professional-End-Of-Lease-Cleaning-Cost-Advantages-and-Disadvantages.webp",
  "https://ozapcs.com.au/wp-content/uploads/2021/03/lease.jpeg",
  "https://sydneyprocleaningservices.com.au/wp-content/uploads/2025/08/Sydney-Professional-Cleaners-7-1024x654.webp",
  "https://a1groupservices.com.au/wp-content/uploads/2023/12/office-cleaning-1024x682.jpg",
  "https://gogreencarpetclean.com.au/wp-content/uploads/2021/08/Carpet-cleaning.jpg",
  "https://www.maid2match.com.au/wp-content/uploads/2021/09/img_services_housecleaning.jpg",
  "https://inandoutwindowcleaning.com.au/wp-content/uploads/2024/02/commercial-window-cleaning1.png"
];

const galleryImages = [
  "https://cleaneffortlessly.com.au/wp-content/uploads/2025/07/about-bg.jpg",
  "https://monstercleaning.com.au/wp-content/uploads/2024/10/Professional-Office-Cleaners-in-Sydney.jpg",
  "https://myercarpetcleaning.com.au/wp-content/uploads/2020/02/Professional-Carpet-Cleaning-Bondi-1.jpg",
  "https://www.resultscleaningco.com/wp-content/uploads/2018/09/residential-Cleaning-Copy-min.jpg",
  "https://www.clearwash.com.au/wp-content/uploads/2020/05/Clearwash-132-scaled.jpg"
];

// Random selection for variety
const profile = profileImages[Math.floor(Math.random() * profileImages.length)];
const photos = [
  galleryImages[Math.floor(Math.random() * galleryImages.length)],
  galleryImages[Math.floor(Math.random() * galleryImages.length)],
  galleryImages[Math.floor(Math.random() * galleryImages.length)]
];

console.log("🌟 Using profile image:", profile);

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
  console.log("🌟 SUCCESS! New post created and will appear in your dashboard:");
  console.log("Title:", blog.title);
  console.log("Live URL: https://www.zoiriscleaningservices.com/blog/" + blog.slug);
} else {
  const err = await supabaseRes.text();
  console.error("Supabase error:", err);
  throw new Error("Insert failed");
}
