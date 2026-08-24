# Product Context: Escuela Anahuac Photo Gallery

## What is this?
A web application for managing and displaying school photography. Teachers/admins upload photos of school activities (academic, sports, cultural events) which are then reviewed and published to a public gallery for parents and the school community.

## Who is it for?
- **Primary**: School administrators and teachers who upload photos
- **Secondary**: Parents, students, and school community who view the public gallery
- **Tertiary**: School leadership who oversee content approval

## Core user flows
1. **Upload flow**: Admin logs in → selects photos → adds caption/category → confirms parent consent → submits for review
2. **Review flow**: Admin views pending photos → approves/rejects/deletes each → approved photos appear in public gallery
3. **View flow**: Anyone visits site → sees approved photos in gallery/album → clicks to view full-size in lightbox
4. **Filter flow**: Album viewer filters by category (All, Academic, Sports, Cultural, General)

## Key constraints
- **Consent-first**: Every upload requires explicit parent consent confirmation
- **Moderation required**: No photo publishes without admin approval
- **Image protection**: Right-click download disabled, watermarking via Cloudinary possible
- **Mobile-first**: Parents primarily view on phones
- **Spanish language**: All UI in Spanish
- **Bootstrap 5**: Current CSS framework (should remain for consistency)

## Brand personality
- **Trustworthy**: School context demands reliability and safety
- **Warm**: Educational environment, family-oriented
- **Professional**: Represents the institution publicly
- **Accessible**: Must work for all ages and technical abilities

## Success metrics
- Time from photo capture to publication < 24 hours
- Zero unauthorized photos published
- Mobile gallery loads in < 3 seconds
- Admin review actions take < 5 seconds per photo