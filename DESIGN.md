# Design System: Escuela Anahuac Photo Gallery

## Color Palette

### Primary - Deep Navy (Trust, Authority)
```css
--color-primary-50:  #e8edf5;
--color-primary-100: #d1dceb;
--color-primary-200: #a3b9d7;
--color-primary-300: #7596c3;
--color-primary-400: #4773af;
--color-primary-500: #1a5091;  /* Main brand */
--color-primary-600: #0d3d73;
--color-primary-700: #092e55;
--color-primary-800: #062037;
--color-primary-900: #03111a;
```

### Secondary - Warm Gold (Warmth, Achievement)
```css
--color-secondary-50:  #fff8e1;
--color-secondary-100: #ffecb3;
--color-secondary-200: #ffe082;
--color-secondary-300: #ffd54f;
--color-secondary-400: #ffca28;
--color-secondary-500: #ffc107;  /* Accent */
--color-secondary-600: #ffb300;
--color-secondary-700: #ffa000;
--color-secondary-800: #ff8f00;
--color-secondary-900: #ff6f00;
```

### Semantic Colors
```css
--color-success: #198754;
--color-success-light: #d1e7dd;
--color-warning: #ffc107;
--color-warning-light: #fff3cd;
--color-danger: #dc3545;
--color-danger-light: #f8d7da;
--color-info: #0dcaf0;
--color-info-light: #cff4fc;
```

### Neutral Scale
```css
--color-neutral-0:   #ffffff;
--color-neutral-50:  #f8f9fa;
--color-neutral-100: #f1f3f5;
--color-neutral-200: #e9ecef;
--color-neutral-300: #dee2e6;
--color-neutral-400: #ced4da;
--color-neutral-500: #adb5bd;
--color-neutral-600: #868e96;
--color-neutral-700: #495057;
--color-neutral-800: #343a40;
--color-neutral-900: #212529;
--color-neutral-950: #0b1f4d;  /* Navbar bg */
```

## Typography

### Font Families
```css
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-display: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', Consolas, monospace;
```

### Type Scale (Fluid, clamp-based)
```css
--text-xs:     clamp(0.7rem, 0.65rem + 0.25vw, 0.75rem);    /* 11-12px */
--text-sm:     clamp(0.8125rem, 0.75rem + 0.3125vw, 0.875rem); /* 13-14px */
--text-base:   clamp(0.9375rem, 0.875rem + 0.3125vw, 1rem);    /* 15-16px */
--text-lg:     clamp(1.0625rem, 1rem + 0.3125vw, 1.125rem);   /* 17-18px */
--text-xl:     clamp(1.25rem, 1.125rem + 0.625vw, 1.5rem);    /* 20-24px */
--text-2xl:    clamp(1.5rem, 1.25rem + 1.25vw, 2rem);         /* 24-32px */
--text-3xl:    clamp(1.875rem, 1.5rem + 1.875vw, 2.5rem);     /* 30-40px */
--text-4xl:    clamp(2.25rem, 1.75rem + 2.5vw, 3rem);         /* 36-48px */
```

### Font Weights
```css
--weight-normal: 400;
--weight-medium: 500;
--weight-semibold: 600;
--weight-bold: 700;
```

### Line Heights
```css
--leading-tight: 1.1;
--leading-snug: 1.375;
--leading-normal: 1.5;
--leading-relaxed: 1.625;
```

## Spacing Scale (8px base)
```css
--space-0: 0;
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-5: 1.25rem;  /* 20px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
--space-10: 2.5rem;  /* 40px */
--space-12: 3rem;    /* 48px */
--space-16: 4rem;    /* 64px */
--space-20: 5rem;    /* 80px */
```

## Border Radius
```css
--radius-none: 0;
--radius-sm: 0.25rem;    /* 4px */
--radius-md: 0.375rem;   /* 6px */
--radius-lg: 0.5rem;     /* 8px */
--radius-xl: 0.75rem;    /* 12px */
--radius-2xl: 1rem;      /* 16px */
--radius-full: 9999px;
```

## Shadows (Layered, purposeful)
```css
--shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
--shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);
```

## Transitions (Meaningful motion)
```css
--duration-fast: 150ms;
--duration-normal: 250ms;
--duration-slow: 350ms;
--ease-out: cubic-bezier(0.16, 1, 0.3, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
```

## Breakpoints
```css
--bp-sm: 640px;
--bp-md: 768px;
--bp-lg: 1024px;
--bp-xl: 1280px;
--bp-2xl: 1536px;
```

## Z-Index Scale
```css
--z-dropdown: 100;
--z-sticky: 200;
--z-fixed: 300;
--z-modal-backdrop: 400;
--z-modal: 500;
--z-popover: 600;
--z-tooltip: 700;
```

## Component Tokens

### Card
```css
--card-bg: var(--color-neutral-0);
--card-border: var(--color-neutral-200);
--card-radius: var(--radius-xl);
--card-shadow: var(--shadow-sm);
--card-shadow-hover: var(--shadow-md);
--card-padding: var(--space-5);
```

### Button
```css
--btn-height-sm: 36px;
--btn-height-md: 44px;  /* Touch target minimum */
--btn-height-lg: 52px;
--btn-padding-x-sm: var(--space-3);
--btn-padding-x-md: var(--space-4);
--btn-padding-x-lg: var(--space-6);
--btn-font-weight: var(--weight-medium);
--btn-radius: var(--radius-md);
--btn-transition: all var(--duration-fast) var(--ease-out);
```

### Form Input
```css
--input-height: 44px;  /* Touch target */
--input-padding-x: var(--space-3);
--input-padding-y: var(--space-2);
--input-font-size: var(--text-base);
--input-border: var(--color-neutral-300);
--input-border-focus: var(--color-primary-500);
--input-bg: var(--color-neutral-0);
--input-radius: var(--radius-md);
--input-placeholder-color: var(--color-neutral-400);
```

### Navbar
```css
--navbar-height: 64px;
--navbar-bg: var(--color-neutral-950);
--navbar-text: var(--color-neutral-0);
--navbar-link-hover: var(--color-neutral-200);
```

### Photo Grid
```css
--photo-aspect: 4/3;
--photo-gap: var(--space-3);
--photo-radius: var(--radius-lg);
--photo-shadow: var(--shadow-sm);
--photo-hover-shadow: var(--shadow-lg);
--photo-hover-scale: 1.02;
```

## Icon System
- Use Bootstrap Icons (already included via CDN)
- Consistent 1rem (16px) for inline, 1.25rem (20px) for standalone
- Stroke width: 2px equivalent

## Accessibility
- Minimum contrast ratio: 4.5:1 (AA) for text, 3:1 for UI elements
- Focus visible: 2px solid var(--color-primary-500) with 2px offset
- Reduced motion: respect prefers-reduced-motion
- Touch targets: minimum 44x44px