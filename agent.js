try {
    let profileUrl = editingPost?.profile || null;
    let photoUrls = editingPost?.photos || [];

    // Upload featured image if new one selected
    if (profileFile) {
        const profileName = `featured_${Date.now()}_${profileFile.name}`;
        const { error: uploadError } = await supabaseClient.storage
            .from('profiles')
            .upload(profileName, profileFile, { upsert: true });

        if (uploadError) throw uploadError;

        const { data: profileData } = supabaseClient.storage
            .from('profiles')
            .getPublicUrl(profileName);

        profileUrl = profileData.publicUrl;
    }

    // Upload gallery photos
    for (const file of photoFiles) {
        if (file) {
            const name = `gallery_${Date.now()}_${file.name}`;
            const { error } = await supabaseClient.storage
                .from('photos')
                .upload(name, file);

            if (error) continue; // skip failed ones

            const { data } = supabaseClient.storage
                .from('photos')
                .getPublicUrl(name);

            photoUrls.push(data.publicUrl);
        }
    }

    // Rest of insert/update code remains the same...
