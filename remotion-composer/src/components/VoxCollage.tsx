import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Img,
} from "remotion";
import { resolveAsset } from "../lib/resolveAsset";

// ============================================================================
// VOX STYLE MASTER SHEET TOKENS
// ============================================================================
export const VOX_COLORS = {
  archivalTan: "#C9BB9C",
  inkBlack: "#1A1A1A",
  halftoneGray: "#8C8C8C",
  hotRed: "#B62E1F",       // Strictly for strokes, underlines, arrows
  mustard: "#D9A441",      // Secondary accent for annotation labels
  paperWhite: "#F8F5EE",
  paperBorder: "#FFFFFF",
  mutedGray: "#5A5A5A",
};

// ============================================================================
// 1. VOX BACKGROUND WITH ARCHIVAL PAPER GRAIN & SLOW 2% DRIFT
// ============================================================================
export const VoxBackground: React.FC<{ children?: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // Slow 2% camera drift (Motion Thumbnail 4)
  const driftScale = interpolate(frame, [0, durationInFrames], [1.0, 1.025], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const driftTranslateY = interpolate(frame, [0, durationInFrames], [0, -8], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: VOX_COLORS.archivalTan,
        overflow: "hidden",
      }}
    >
      {/* Drifting Layer containing Grid and Map Elements */}
      <div
        style={{
          position: "absolute",
          inset: -40,
          transform: `scale(${driftScale}) translateY(${driftTranslateY}px)`,
          transformOrigin: "center center",
          willChange: "transform",
        }}
      >
        {/* Halftone & Map Texture Layer */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            backgroundImage: `
              radial-gradient(${VOX_COLORS.halftoneGray} 1.2px, transparent 1.2px),
              linear-gradient(rgba(26,26,26,0.06) 1px, transparent 1px),
              linear-gradient(90deg, rgba(26,26,26,0.06) 1px, transparent 1px)
            `,
            backgroundSize: "16px 16px, 120px 120px, 120px 120px",
            opacity: 0.75,
          }}
        />

        {/* Archival Framing Borders */}
        <div
          style={{
            position: "absolute",
            inset: 48,
            border: `2px solid rgba(26,26,26,0.25)`,
            pointerEvents: "none",
          }}
        >
          <div
            style={{
              position: "absolute",
              inset: 8,
              border: `1px dashed rgba(26,26,26,0.18)`,
            }}
          />
        </div>
      </div>

      {/* Foreground Content */}
      <div style={{ position: "absolute", inset: 0 }}>
        {children}
      </div>
    </AbsoluteFill>
  );
};

// ============================================================================
// 2. VOX HEADLINE (Condensed Ink-Black with Animated Red Underline Swipe)
// ============================================================================
export const VoxHeadline: React.FC<{
  title: string;
  subtitle?: string;
  fontSize?: number;
  align?: "left" | "center";
}> = ({ title, subtitle, fontSize = 72, align = "left" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Red underline swipes in (Motion Thumbnail 3)
  const underlineProgress = spring({
    frame: frame - 6,
    fps,
    config: { damping: 14, stiffness: 100 },
  });

  const textSpring = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 140 },
  });

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: align === "center" ? "center" : "flex-start",
        width: "100%",
      }}
    >
      <div
        style={{
          fontFamily: "Impact, 'Space Grotesk', -apple-system, sans-serif",
          fontSize,
          fontWeight: 900,
          color: VOX_COLORS.inkBlack,
          textTransform: "uppercase",
          letterSpacing: "-0.02em",
          lineHeight: 1.05,
          opacity: textSpring,
          transform: `translateY(${interpolate(textSpring, [0, 1], [24, 0])}px)`,
          textAlign: align,
        }}
      >
        {title}
      </div>

      {/* Hot Red Underline Swipe */}
      <div
        style={{
          height: 6,
          backgroundColor: VOX_COLORS.hotRed,
          marginTop: 10,
          width: `${interpolate(underlineProgress, [0, 1], [0, 100])}%`,
          maxWidth: align === "center" ? 480 : "100%",
          borderRadius: 2,
        }}
      />

      {subtitle && (
        <div
          style={{
            fontFamily: "Inter, system-ui, sans-serif",
            fontSize: Math.round(fontSize * 0.38),
            fontWeight: 600,
            color: VOX_COLORS.inkBlack,
            marginTop: 14,
            opacity: interpolate(frame, [10, 24], [0, 0.9], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }),
            letterSpacing: "0.02em",
            textAlign: align,
          }}
        >
          {subtitle}
        </div>
      )}
    </div>
  );
};

// ============================================================================
// 3. VOX ANNOTATION BADGE ("Fig. 3 - Trade Route" Mustard Badge)
// ============================================================================
export const VoxAnnotationBadge: React.FC<{
  label: string;
  figureNumber?: number | string;
  accentColor?: string;
}> = ({ label, figureNumber = 1, accentColor = VOX_COLORS.mustard }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const popSpring = spring({
    frame: frame - 12,
    fps,
    config: { damping: 12, stiffness: 150 },
  });

  return (
    <div
      style={{
        display: "inline-flex",
        alignItems: "center",
        backgroundColor: accentColor,
        border: `2px solid ${VOX_COLORS.inkBlack}`,
        boxShadow: `4px 4px 0px ${VOX_COLORS.inkBlack}`,
        padding: "6px 16px",
        borderRadius: 2,
        transform: `scale(${popSpring}) rotate(-1.5deg)`,
        opacity: popSpring,
        willChange: "transform, opacity",
      }}
    >
      <span
        style={{
          fontFamily: "'Courier New', Courier, monospace",
          fontSize: 22,
          fontWeight: 800,
          color: VOX_COLORS.inkBlack,
          textTransform: "uppercase",
          letterSpacing: "0.06em",
        }}
      >
        Fig. {figureNumber} — {label}
      </span>
    </div>
  );
};

// ============================================================================
// 4. VOX CUTOUT CONTAINER (White sticker outline + 6px offset red stroke)
// ============================================================================
export const VoxCutout: React.FC<{
  children: React.ReactNode;
  delay?: number;
  rotation?: number;
  offsetColor?: string;
}> = ({ children, delay = 0, rotation = 0, offsetColor = VOX_COLORS.hotRed }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Cutout springs up with overshoot (Motion Thumbnail 1)
  const springProgress = spring({
    frame: frame - delay,
    fps,
    config: { damping: 11, stiffness: 125, mass: 1 },
  });

  const translateY = interpolate(springProgress, [0, 1], [90, 0]);
  const scale = interpolate(springProgress, [0, 1], [0.85, 1.0]);

  return (
    <div
      style={{
        display: "inline-block",
        transform: `translateY(${translateY}px) scale(${scale}) rotate(${rotation}deg)`,
        filter: `drop-shadow(8px 8px 0px ${offsetColor})`,
        willChange: "transform",
      }}
    >
      <div
        style={{
          border: `4px solid ${VOX_COLORS.paperBorder}`,
          backgroundColor: VOX_COLORS.paperWhite,
          boxShadow: `0 0 0 2px ${VOX_COLORS.inkBlack}`,
          overflow: "hidden",
        }}
      >
        {children}
      </div>
    </div>
  );
};

// ============================================================================
// 5. VOX STAT HERO (Big bold counter with red/black box & tick-up)
// ============================================================================
export const VoxStatHero: React.FC<{
  targetValue: number;
  prefix?: string;
  suffix?: string;
  label?: string;
  isNegative?: boolean;
}> = ({ targetValue, prefix = "", suffix = "", label, isNegative = false }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Counter ticks upward (Motion Thumbnail 2)
  const tickProgress = spring({
    frame: frame - 8,
    fps,
    config: { damping: 18, stiffness: 65 },
  });

  const currentValue = Math.round(interpolate(tickProgress, [0, 1], [0, targetValue]));
  const formattedVal = Math.abs(currentValue).toLocaleString();
  const displayVal = `${prefix}${isNegative ? "-" : ""}${formattedVal}${suffix}`;

  return (
    <VoxCutout offsetColor={VOX_COLORS.hotRed} rotation={1.5}>
      <div
        style={{
          padding: "36px 48px",
          textAlign: "center",
          minWidth: 320,
          backgroundColor: VOX_COLORS.paperWhite,
        }}
      >
        <div
          style={{
            fontFamily: "Impact, 'Space Grotesk', sans-serif",
            fontSize: 108,
            fontWeight: 900,
            color: isNegative ? VOX_COLORS.hotRed : VOX_COLORS.inkBlack,
            lineHeight: 1.0,
            letterSpacing: "-0.03em",
          }}
        >
          {displayVal}
        </div>
        {label && (
          <div
            style={{
              fontFamily: "'Courier New', Courier, monospace",
              fontSize: 22,
              fontWeight: 800,
              color: VOX_COLORS.inkBlack,
              marginTop: 16,
              textTransform: "uppercase",
              letterSpacing: "0.08em",
              borderTop: `2px solid ${VOX_COLORS.inkBlack}`,
              paddingTop: 10,
            }}
          >
            {label}
          </div>
        )}
      </div>
    </VoxCutout>
  );
};

// ============================================================================
// 6. VOX RED ARROW (Animated Hot Red Directional Line / Arrow)
// ============================================================================
export const VoxRedArrow: React.FC<{
  length?: number;
  angle?: number;
  delay?: number;
}> = ({ length = 160, angle = 0, delay = 10 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const arrowDraw = spring({
    frame: frame - delay,
    fps,
    config: { damping: 14, stiffness: 120 },
  });

  const arrowHeadScale = spring({
    frame: frame - delay - 6,
    fps,
    config: { damping: 10, stiffness: 150 },
  });

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        transform: `rotate(${angle}deg)`,
        transformOrigin: "left center",
      }}
    >
      <div
        style={{
          height: 6,
          backgroundColor: VOX_COLORS.hotRed,
          width: interpolate(arrowDraw, [0, 1], [0, length]),
          borderRadius: 2,
        }}
      />
      {/* Arrowhead */}
      <div
        style={{
          width: 0,
          height: 0,
          borderTop: "12px solid transparent",
          borderBottom: "12px solid transparent",
          borderLeft: `18px solid ${VOX_COLORS.hotRed}`,
          marginLeft: -2,
          transform: `scale(${arrowHeadScale})`,
          opacity: arrowHeadScale,
        }}
      />
    </div>
  );
};
