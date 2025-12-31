async function generateAndPublishAI() {
    if (isPublishing) return;
    isPublishing = true;
    msg.innerHTML = '<p style="color:#ffeb3b;">Generating AI blog post...</p>';

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

    try {
        const aiRes = await fetch(
            `https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${YOUR_GEMINI_API_KEY}`,
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
            throw new Error(`Gemini API error: ${await aiRes.text()}`);
        }

        const aiData = await aiRes.json();
        const textResponse = aiData.candidates[0].content.parts[0].text;
        const blog = JSON.parse(textResponse);

        // Use default images if you want
        const profileUrl = "https://via.placeholder.com/600x400/0d9488/ffffff?text=Featured+Image";
        const photoUrls = [
            "https://via.placeholder.com/400x300/0d9488/ffffff?text=Gallery+1",
            "https://via.placeholder.com/400x300/0d9488/ffffff?text=Gallery+2",
            "https://via.placeholder.com/400x300/0d9488/ffffff?text=Gallery+3"
        ];

        const cleanSlug = blog.slug
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-+|-+$/g, '')
            .substring(0, 80);

        const postData = {
            id: crypto.randomUUID(),
            name: blog.title,
            description: blog.content,
            profile: profileUrl,
            photos: photoUrls,
            slug: cleanSlug,
            created_at: new Date().toISOString()
        };

        const { error } = await supabaseClient.from('services').insert(postData);
        if (error) throw error;

        msg.innerHTML = `
            <p style="color:#0f0; font-weight:bold;">
                AI-generated post published successfully!<br>
                View it live at:<br>
                <a href="${BLOG_BASE_URL}${BASE_PATH}/${cleanSlug}" target="_blank" style="color:#ffeb3b; font-size:1.1em;">
                    ${BLOG_BASE_URL}${BASE_PATH}/${cleanSlug}
                </a>
            </p>
        `;

        loadMyPosts();
    } catch (err) {
        console.error(err);
        msg.innerHTML = `<p style="color:red;">Error generating AI post: ${err.message}</p>`;
    } finally {
        isPublishing = false;
    }
}

// Optional: Add a button to dashboard to generate AI post
const aiButton = document.createElement('button');
aiButton.textContent = 'Generate AI Blog Post';
aiButton.style.cssText = 'margin:20px auto; display:block; padding:12px 24px; background:#0d9488; color:white; border:none; border-radius:16px; cursor:pointer; font-weight:bold;';
aiButton.onclick = generateAndPublishAI;
document.querySelector('.main-content').prepend(aiButton);
