# 🎨 UI/UX Design Specification - Wall Street Meets Cyberpunk

**Project:** Ultimate Anonymity Toolkit - Tauri GUI  
**Design Theme:** Professional Trading Terminal + Cyberpunk Aesthetics  
**Created:** 2025-10-04  
**Status:** Design Phase

---

## 🎯 **DESIGN PHILOSOPHY**

### **Core Principles**

1. **Professional First, Cyberpunk Second**
   - Clean, organized layouts like Bloomberg Terminal
   - Information density without clutter
   - Cyberpunk aesthetics as accents, not overwhelming

2. **Dark Mode Native**
   - All interfaces designed for dark theme
   - High contrast for readability
   - Reduced eye strain for extended use

3. **Neon Accents for Hierarchy**
   - Neon colors guide user attention
   - CTAs (Call-to-Actions) use bright neon
   - Status indicators use semantic neon colors

4. **Glassmorphism for Depth**
   - Frosted glass effect creates visual hierarchy
   - Subtle blur for layered interfaces
   - Transparency shows depth and context

5. **Subtle Animations**
   - Smooth, professional transitions
   - No jarring or distracting movements
   - Animations enhance UX, not just decoration

---

## 🎨 **COLOR PALETTE**

### **Primary Colors - Cyberpunk Neon**

```css
/* Electric Cyan - Primary Brand Color */
--neon-cyan: #00FFFF;
--neon-cyan-rgb: 0, 255, 255;
Use: Primary buttons, links, active states, brand elements

/* Deep Violet - Secondary Accent */
--neon-purple: #9201CB;
--neon-purple-rgb: 146, 1, 203;
Use: Secondary buttons, highlights, special features

/* Hollywood Cerise - Alerts & Warnings */
--neon-pink: #F715AB;
--neon-pink-rgb: 247, 21, 171;
Use: Warnings, errors, critical alerts, danger actions

/* Zaffre Blue - Interactive Elements */
--neon-blue: #0313A6;
--neon-blue-rgb: 3, 19, 166;
Use: Links, hover states, info messages

/* Electric Green - Success States */
--electric-green: #39FF14;
--electric-green-rgb: 57, 255, 20;
Use: Success messages, active status, confirmations
```

### **Base Colors - Wall Street Professional**

```css
/* Deep Navy - Main Background */
--dark-bg: #0A0E27;
--dark-bg-rgb: 10, 14, 39;
Use: Main app background, body background

/* Oxford Blue - Cards & Panels */
--darker-bg: #070F34;
--darker-bg-rgb: 7, 15, 52;
Use: Card backgrounds, elevated surfaces

/* Charcoal - Elevated Surfaces */
--charcoal: #1A1F3A;
--charcoal-rgb: 26, 31, 58;
Use: Modals, dropdowns, tooltips

/* Slate - Borders & Dividers */
--slate: #2D3250;
--slate-rgb: 45, 50, 80;
Use: Borders, dividers, separators
```

### **Text Colors**

```css
/* High Contrast White - Primary Text */
--text-primary: #E8E9ED;
--text-primary-rgb: 232, 233, 237;
Use: Headings, important text, labels

/* Muted Text - Secondary Text */
--text-secondary: #A0A3BD;
--text-secondary-rgb: 160, 163, 189;
Use: Descriptions, secondary info, metadata

/* Disabled Text - Placeholder */
--text-muted: #6B7280;
--text-muted-rgb: 107, 114, 128;
Use: Disabled text, placeholders, hints
```

### **Semantic Colors**

```css
/* Success - Green */
--success: #10B981;
--success-rgb: 16, 185, 129;

/* Warning - Amber */
--warning: #F59E0B;
--warning-rgb: 245, 158, 11;

/* Error - Red */
--error: #EF4444;
--error-rgb: 239, 68, 68;

/* Info - Blue */
--info: #3B82F6;
--info-rgb: 59, 130, 246;
```

---

## 🔤 **TYPOGRAPHY**

### **Font Families**

```css
/* Headings - Bold, Modern, Tech */
--font-heading: 'Orbitron', 'Rajdhani', 'Exo 2', sans-serif;
Use: Page titles, section headers, card titles
Weight: 700 (Bold), 900 (Black)
Characteristics: Geometric, futuristic, tech-inspired

/* Body - Clean, Readable, Professional */
--font-body: 'Inter', 'Roboto', 'SF Pro Display', sans-serif;
Use: Body text, descriptions, paragraphs
Weight: 400 (Regular), 500 (Medium), 600 (Semi-bold)
Characteristics: Highly readable, professional, modern

/* Monospace - Code, Data, Terminal */
--font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
Use: Code snippets, IP addresses, technical data, logs
Weight: 400 (Regular), 700 (Bold)
Characteristics: Monospaced, ligatures, coding-optimized
```

### **Font Sizes**

```css
/* Display - Hero Text */
--text-display: 3.5rem;    /* 56px */
--text-display-line: 1.1;

/* H1 - Page Titles */
--text-h1: 2.5rem;         /* 40px */
--text-h1-line: 1.2;

/* H2 - Section Headers */
--text-h2: 2rem;           /* 32px */
--text-h2-line: 1.3;

/* H3 - Card Titles */
--text-h3: 1.5rem;         /* 24px */
--text-h3-line: 1.4;

/* H4 - Subsection Headers */
--text-h4: 1.25rem;        /* 20px */
--text-h4-line: 1.5;

/* Body - Regular Text */
--text-body: 1rem;         /* 16px */
--text-body-line: 1.6;

/* Small - Metadata */
--text-small: 0.875rem;    /* 14px */
--text-small-line: 1.5;

/* Tiny - Labels */
--text-tiny: 0.75rem;      /* 12px */
--text-tiny-line: 1.4;
```

---

## ✨ **VISUAL EFFECTS**

### **Glassmorphism**

```css
/* Glass Card - Standard */
.glass-card {
  background: rgba(26, 31, 58, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 12px;
}

/* Glass Card - Elevated */
.glass-card-elevated {
  background: rgba(26, 31, 58, 0.8);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Glass Modal */
.glass-modal {
  background: rgba(7, 15, 52, 0.9);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.4);
}
```

### **Neon Glow Effects**

```css
/* Cyan Glow */
.glow-cyan {
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.5),
              0 0 40px rgba(0, 255, 255, 0.3),
              0 0 60px rgba(0, 255, 255, 0.1);
}

/* Purple Glow */
.glow-purple {
  box-shadow: 0 0 20px rgba(146, 1, 203, 0.5),
              0 0 40px rgba(146, 1, 203, 0.3),
              0 0 60px rgba(146, 1, 203, 0.1);
}

/* Pink Glow */
.glow-pink {
  box-shadow: 0 0 20px rgba(247, 21, 171, 0.5),
              0 0 40px rgba(247, 21, 171, 0.3),
              0 0 60px rgba(247, 21, 171, 0.1);
}

/* Subtle Glow - For Hover States */
.glow-subtle {
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
}
```

### **Animations**

```css
/* Pulse Glow - For Active Elements */
@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
  }
  50% {
    box-shadow: 0 0 40px rgba(0, 255, 255, 0.8);
  }
}

/* Slide Up - For Cards */
@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Fade In - For Text */
@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Shimmer - For Loading States */
@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}
```

### **Scanline Effect (Optional)**

```css
/* Subtle Scanline Overlay - Cyberpunk Atmosphere */
.scanlines::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    to bottom,
    transparent 50%,
    rgba(0, 255, 255, 0.02) 50%
  );
  background-size: 100% 4px;
  pointer-events: none;
  z-index: 1000;
}
```

---

## 🧩 **COMPONENT LIBRARY**

### **Buttons**

```tsx
// Primary Button - Neon Cyan
<button className="
  px-6 py-3 
  bg-neon-cyan text-dark-bg 
  font-heading font-bold 
  rounded-md 
  hover:shadow-glow-cyan 
  transition-all duration-300
  hover:scale-105
">
  Launch Browser
</button>

// Secondary Button - Outlined
<button className="
  px-6 py-3 
  border-2 border-neon-cyan text-neon-cyan 
  font-heading font-bold 
  rounded-md 
  hover:bg-neon-cyan hover:text-dark-bg 
  transition-all duration-300
">
  Run Leak Test
</button>

// Danger Button - Neon Pink
<button className="
  px-6 py-3 
  bg-neon-pink text-white 
  font-heading font-bold 
  rounded-md 
  hover:shadow-glow-pink 
  transition-all duration-300
">
  Terminate Session
</button>
```

### **Cards**

```tsx
// Glass Card - Standard
<div className="
  backdrop-blur-md 
  bg-dark-charcoal/70 
  border border-neon-cyan/20 
  rounded-lg 
  p-6
  hover:border-neon-cyan/40
  transition-all duration-300
">
  <h3 className="font-heading text-xl text-neon-cyan mb-4">
    Profile Mode
  </h3>
  <p className="font-body text-text-secondary">
    Persistent identity with consistent fingerprint
  </p>
</div>

// Metric Card - With Glow
<div className="
  backdrop-blur-md 
  bg-dark-charcoal/70 
  border border-neon-cyan/20 
  rounded-lg 
  p-6
  shadow-glow-cyan
">
  <div className="text-4xl font-heading text-neon-cyan mb-2">
    98%
  </div>
  <div className="text-sm font-body text-text-secondary">
    Anonymity Score
  </div>
</div>
```

### **Status Indicators**

```tsx
// Active Status - Green Glow
<div className="flex items-center gap-2">
  <div className="
    w-3 h-3 
    rounded-full 
    bg-electric-green 
    shadow-[0_0_10px_rgba(57,255,20,0.8)]
    animate-pulse
  "></div>
  <span className="font-mono text-sm text-electric-green">
    ACTIVE
  </span>
</div>

// Warning Status - Amber
<div className="flex items-center gap-2">
  <div className="
    w-3 h-3 
    rounded-full 
    bg-warning 
    shadow-[0_0_10px_rgba(245,158,11,0.8)]
    animate-pulse
  "></div>
  <span className="font-mono text-sm text-warning">
    WARNING
  </span>
</div>

// Error Status - Red
<div className="flex items-center gap-2">
  <div className="
    w-3 h-3 
    rounded-full 
    bg-error 
    shadow-[0_0_10px_rgba(239,68,68,0.8)]
    animate-pulse
  "></div>
  <span className="font-mono text-sm text-error">
    ERROR
  </span>
</div>
```

### **Data Tables**

```tsx
// Trading Terminal Style Table
<table className="w-full font-mono text-sm">
  <thead>
    <tr className="border-b border-neon-cyan/20">
      <th className="text-left py-3 text-neon-cyan font-heading">
        Session ID
      </th>
      <th className="text-left py-3 text-neon-cyan font-heading">
        Browser
      </th>
      <th className="text-left py-3 text-neon-cyan font-heading">
        Duration
      </th>
      <th className="text-left py-3 text-neon-cyan font-heading">
        Status
      </th>
    </tr>
  </thead>
  <tbody>
    <tr className="border-b border-slate/20 hover:bg-charcoal/30">
      <td className="py-3 text-text-primary">session_001</td>
      <td className="py-3 text-text-secondary">Chrome</td>
      <td className="py-3 text-text-secondary">2m 34s</td>
      <td className="py-3">
        <span className="text-electric-green">● ACTIVE</span>
      </td>
    </tr>
  </tbody>
</table>
```

---

## 📐 **LAYOUT SYSTEM**

### **Grid System**

```css
/* 12-Column Grid */
.grid-12 {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1.5rem;
}

/* Common Layouts */
.layout-sidebar {
  grid-template-columns: 250px 1fr;
}

.layout-3-col {
  grid-template-columns: repeat(3, 1fr);
}

.layout-2-col {
  grid-template-columns: repeat(2, 1fr);
}
```

### **Spacing Scale**

```css
--space-xs: 0.25rem;   /* 4px */
--space-sm: 0.5rem;    /* 8px */
--space-md: 1rem;      /* 16px */
--space-lg: 1.5rem;    /* 24px */
--space-xl: 2rem;      /* 32px */
--space-2xl: 3rem;     /* 48px */
--space-3xl: 4rem;     /* 64px */
```

### **Border Radius**

```css
--radius-sm: 0.375rem;  /* 6px */
--radius-md: 0.5rem;    /* 8px */
--radius-lg: 0.75rem;   /* 12px */
--radius-xl: 1rem;      /* 16px */
--radius-full: 9999px;  /* Fully rounded */
```

---

## 🎬 **ANIMATION GUIDELINES**

### **Timing Functions**

```css
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

### **Duration Standards**

```css
--duration-fast: 150ms;     /* Quick feedback */
--duration-normal: 300ms;   /* Standard transitions */
--duration-slow: 500ms;     /* Emphasis animations */
```

### **Animation Principles**

1. **Purposeful** - Every animation serves a UX purpose
2. **Consistent** - Same timing for similar interactions
3. **Subtle** - Professional, not distracting
4. **Performant** - Use transform and opacity for 60fps

---

## 🖼️ **ICON SYSTEM**

### **Icon Library: Lucide React**

```tsx
import { 
  Shield, Lock, Eye, EyeOff,
  Activity, TrendingUp, AlertTriangle,
  Settings, User, Globe, Wifi,
  Play, Pause, Stop, RefreshCw,
  CheckCircle, XCircle, Info
} from 'lucide-react';

// Usage
<Shield className="w-6 h-6 text-neon-cyan" />
```

### **Icon Sizes**

```css
--icon-xs: 1rem;    /* 16px */
--icon-sm: 1.25rem; /* 20px */
--icon-md: 1.5rem;  /* 24px */
--icon-lg: 2rem;    /* 32px */
--icon-xl: 3rem;    /* 48px */
```

---

## 📱 **RESPONSIVE DESIGN**

### **Breakpoints**

```css
--screen-sm: 640px;   /* Mobile landscape */
--screen-md: 768px;   /* Tablet */
--screen-lg: 1024px;  /* Desktop */
--screen-xl: 1280px;  /* Large desktop */
--screen-2xl: 1536px; /* Extra large */
```

### **Mobile Adaptations**

- Stack cards vertically on mobile
- Reduce font sizes by 10-15%
- Simplify glassmorphism effects
- Reduce glow intensity
- Hide non-essential animations

---

## 🎯 **ACCESSIBILITY**

### **WCAG 2.1 AA Compliance**

- **Contrast Ratios:**
  - Text on dark background: 7:1 minimum
  - Large text: 4.5:1 minimum
  - Interactive elements: 3:1 minimum

- **Keyboard Navigation:**
  - All interactive elements focusable
  - Visible focus indicators
  - Logical tab order

- **Screen Readers:**
  - Semantic HTML
  - ARIA labels where needed
  - Alt text for images

---

**Last Updated:** 2025-10-04  
**Next Review:** After initial implementation  
**Maintained By:** Design Team

