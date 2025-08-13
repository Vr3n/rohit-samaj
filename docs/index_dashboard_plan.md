# Plan for Index Dashboard

Thought for 3sRead codebase structureThought for 3s### Samaaj Member Dashboard - Implementation Guide

## Overview

Create a mobile-first responsive dashboard for Samaaj (community) member management system. This is the first page users see after signup, focusing on profile completion tracking and member management.

## UI Implementation Steps

### 1. Layout Structure

- Use `min-h-screen bg-gray-50 p-4 space-y-6` for main container
- Implement mobile-first approach with 4px padding
- Use consistent 6-unit spacing between sections

### 2. Header Section

- Center-aligned title "समाज सदस्य डैशबोर्ड" with `text-2xl font-bold`
- Personalized greeting with user's name

### 3. Profile Completion Alert

- Conditional rendering when profile incomplete
- Orange color scheme (`border-orange-200 bg-orange-50`)
- Include AlertCircle icon and completion percentage
- Add call-to-action button

### 4. Progress Visualization

- **Progress Bar**: Use shadcn Progress component with calculated percentage
- **Pie Chart**: Implement with Recharts

- Inner radius: 40px, Outer radius: 70px
- Green for completed (`#10b981`), Gray for incomplete (`#f3f4f6`)
- Include tooltip and legend

- **Section Status Grid**: List all 7 sections with completion badges

### 5. Action Buttons

- Two full-width buttons in single column grid
- Primary: (blue, with UserPlus icon)
- Secondary: (outline, with Eye icon)
- Height: 56px (`h-14`) for better mobile touch targets

### 6. Member Metrics Grid

- 2x2 grid layout (`grid-cols-2 gap-4`)
- Color-coded metric cards:

- Total members: Blue theme
- This month: Green theme
- This week: Purple theme
- Pending approvals: Orange theme

- Large number display (`text-2xl font-bold`) with descriptive labels

### 7. Quick Actions Footer

- Simple card with horizontal layout
- Users icon with xt
- Arrow link for additional options

## Mobile-First Design Principles

### Touch Targets

- Minimum 44px height for all interactive elements
- Use `h-14` (56px) for primary buttons
- Adequate spacing between clickable elements

### Typography

- Use system fonts (Geist Sans/Mono)
- Maintain readable font sizes (minimum 14px)
- Clear visual hierarchy with font weights

### Spacing & Layout

- Consistent 4px base padding
- Use Tailwind spacing scale (space-y-6, gap-4, etc.)
- Single column layout for mobile optimization

### Color Accessibility

- Maintain WCAG contrast ratios
- Use semantic colors (green=complete, orange=warning, blue=primary)
- Test in both light and dark modes

## Responsive Behavior

- Default: Single column layout
- All grids collapse to single column on mobile
- Cards stack vertically with consistent spacing
- Text remains readable at all screen sizes

## Internationalization Notes

- Cultural color associations (saffron, blue themes)

This dashboard prioritizes mobile usability with large touch targets, clear visual hierarchy, and essential functionality prominently displayed.\
The design uses familiar patterns while incorporating cultural elements appropriate for the Indian market.
