// agent.js
import fetch from 'node-fetch';
import OpenAI from 'openai';
import { createClient } from '@supabase/supabase-js';
import crypto from 'crypto';

// Initialize OpenAI & Supabase
const openai = new OpenAI({ apiKey: process.env.GEMINI_API_KEY });
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

async function generateBlogPost() {
  const prompt = `
Write a fully SEO-optimized blog post about Zoiris Cleaning Services in Mobile, AL.
Include the business phone number (251-930-8621) and email (zoiriscleaningservices@gmail.com).
Include headings, subheadings, and keywords relevant to residential and commercial cleaning.
Suggest 3 images (featured + gallery) and provide them as URLs.
Return JSON like:
{
  "title": "...",
  "content": "...",
  "images": ["url1","url2","url3"]
}
  `;

  const aiResponse = await openai.chat.completions.create({
    model: "gpt-5-mini",
    messages: [{ role: "user", content: prompt }],
  });

  const post = JSON.parse(aiResponse.choices[0].message.content);
  return post;
}

async function uploadImageFromURL(url, folder) {
  const response = await fetch(url);
  const buffer = await response.arrayBuffer();
  const fileName = `${folder}_${crypto.randomUUID()}.jpg`;
  const { error } = await supabase.storage.from(folder).upload(fileName, Buffer.from(buffer), { upsert: true });
  if (error) throw error;

  const { data } = supabase.storage.from(folder).getPublicUrl(fileName);
  return data.publicUrl;
}

async function runAgent() {
  try {
    console.log("Generating AI blog post...");
    const post = await generateBlogPost();

    console.log("Uploading images...");
    const profileUrl = await uploadImageFromURL(post.images[0], "profiles");
    const photoUrls = [];
    for (let i = 1; i < post.images.length; i++) {
      const url = await uploadImageFromURL(post.images[i], "photos");
      photoUrls.push(url);
    }

    const slug = post.title.toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
      .substring(0, 80);

    console.log("Inserting post into Supabase...");
    await supabase.from('services').insert({
      id: crypto.randomUUID(),
      name: post.title,
      description: post.content,
      profile: profileUrl,
      photos: photoUrls.length ? photoUrls : null,
      slug,
      created_at: new Date().toISOString()
    });

    console.log("✅ AI blog post created successfully!");
  } catch (err) {
    console.error("❌ Error creating blog post:", err);
  }
}

runAgent();
