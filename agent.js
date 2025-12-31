const postData = {
    name: title,
    description: content,
    profile: profileUrl,
    photos: photoUrls.length ? photoUrls : null,
    slug: cleanSlug,
    created_at: editingPost ? editingPost.created_at : new Date().toISOString()
};

if (editingPost) {
    await supabaseClient
        .from('services')
        .update(postData)
        .eq('id', editingPost.id);
} else {
    postData.id = crypto.randomUUID();
    await supabaseClient.from('services').insert(postData);
}
