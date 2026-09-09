import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import {
  VoxBackground,
  VoxHeadline,
  VoxAnnotationBadge,
  VoxCutout,
  VoxStatHero,
  VoxRedArrow,
  VOX_COLORS,
} from "./components/VoxCollage";
import { resolveAsset } from "./lib/resolveAsset";

export interface VoxSceneCut {
  id: string;
  scene_number: number;
  in_seconds: number;
  out_seconds: number;
  visualType: string;
  headline: string;
  subtitle?: string;
  figureLabel: string;
  figureNumber: number;
  statNumber: number;
  statPrefix?: string;
  statSuffix?: string;
  statLabel?: string;
  isNegative?: boolean;
  voiceoverText?: string;
  alertText?: string;
  audioSrc?: string;
  durationSeconds?: number;
}

export interface VoxExplainerProps {
  [key: string]: unknown;
  cuts: VoxSceneCut[];
  audio?: {
    narration?: { src: string; volume?: number };
    music?: { src: string; volume?: number };
  };
}

// ============================================================================
// LOWER THIRD NEWSROOM SYNCHRONIZED KARAOKE CAPTION OVERLAY
// ============================================================================
const VoxCaptionOverlay: React.FC<{ text?: string; durationSeconds?: number }> = ({
  text,
  durationSeconds = 6.0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (!text) return null;

  const currentSec = frame / fps;
  const words = text.split(/\s+/).filter(Boolean);

  // Compute weight per word based on character length for natural pacing
  const weights = words.map((w) => Math.max(3, w.length));
  const totalWeight = weights.reduce((a, b) => a + b, 0);

  // Active speech window: starts at 0.15s, finishes 0.20s before cut ends
  const speechStart = 0.15;
  const speechEnd = Math.max(speechStart + 1.0, durationSeconds - 0.20);
  const speechDur = speechEnd - speechStart;

  let cumulative = 0;
  const wordTimings = words.map((word, i) => {
    const startFrac = cumulative / totalWeight;
    cumulative += weights[i];
    const endFrac = cumulative / totalWeight;
    return {
      word,
      startSec: speechStart + startFrac * speechDur,
      endSec: speechStart + endFrac * speechDur,
    };
  });

  const captionSpring = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 120 },
  });

  return (
    <div
      style={{
        position: "absolute",
        bottom: 30,
        left: 50,
        right: 50,
        backgroundColor: "rgba(248, 245, 238, 0.98)",
        border: `3px solid ${VOX_COLORS.inkBlack}`,
        boxShadow: `6px 6px 0px ${VOX_COLORS.hotRed}`,
        padding: "16px 22px",
        zIndex: 20,
        transform: `translateY(${interpolate(captionSpring, [0, 1], [30, 0])}px)`,
        opacity: captionSpring,
      }}
    >
      <div
        style={{
          fontFamily: "'Courier New', Courier, monospace",
          fontSize: 15,
          fontWeight: 800,
          color: VOX_COLORS.hotRed,
          textTransform: "uppercase",
          letterSpacing: "0.08em",
          marginBottom: 8,
          display: "flex",
          alignItems: "center",
          gap: 8,
        }}
      >
        <span style={{ display: "inline-block", width: 8, height: 8, borderRadius: "50%", backgroundColor: VOX_COLORS.hotRed }} />
        VOX DOCUMENTARY NARRATION:
      </div>
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "6px 8px",
          alignItems: "center",
        }}
      >
        {wordTimings.map((wt, i) => {
          const isCurrent = currentSec >= wt.startSec && currentSec < wt.endSec;
          const isPast = currentSec >= wt.endSec;
          return (
            <span
              key={i}
              style={{
                fontFamily: "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
                fontSize: 25,
                fontWeight: isCurrent ? 800 : isPast ? 700 : 500,
                color: isCurrent ? "#FFFFFF" : isPast ? VOX_COLORS.inkBlack : "rgba(26, 26, 26, 0.35)",
                backgroundColor: isCurrent ? VOX_COLORS.hotRed : "transparent",
                padding: isCurrent ? "2px 6px" : "2px 0px",
                borderRadius: 4,
                boxShadow: isCurrent ? `2px 2px 0px ${VOX_COLORS.inkBlack}` : "none",
                transform: isCurrent ? "scale(1.08)" : "scale(1.0)",
                display: "inline-block",
                transition: "all 0.08s ease-out",
                lineHeight: 1.35,
              }}
            >
              {wt.word}
            </span>
          );
        })}
      </div>
    </div>
  );
};

// ============================================================================
// 1. HOOK / STAT SCENE: Retail Trap & Breakout Illusion
// ============================================================================
const VoxHookStatScene: React.FC<{ cut: VoxSceneCut }> = ({ cut }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const stampSpring = spring({
    frame: frame - 16,
    fps,
    config: { damping: 10, stiffness: 140 },
  });

  return (
    <AbsoluteFill style={{ padding: "80px 60px 170px", justifyContent: "space-between" }}>
      <div>
        <div style={{ marginBottom: 18 }}>
          <VoxAnnotationBadge figureNumber={cut.figureNumber} label={cut.figureLabel} />
        </div>
        <VoxHeadline title={cut.headline} subtitle={cut.subtitle} fontSize={74} />
      </div>

      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-around",
          margin: "30px 0",
        }}
      >
        <VoxCutout delay={4} rotation={-2} offsetColor={VOX_COLORS.hotRed}>
          <div style={{ width: 260, height: 420, overflow: "hidden", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <Img
              src={resolveAsset("assets/vintage_trader.svg")}
              style={{ width: "100%", height: "100%", objectFit: "contain" }}
            />
          </div>
        </VoxCutout>

        <div style={{ margin: "0 10px" }}>
          <VoxRedArrow length={130} angle={0} delay={12} />
        </div>

        <VoxStatHero
          targetValue={cut.statNumber}
          suffix={cut.statSuffix || "%"}
          prefix={cut.statPrefix || ""}
          label={cut.statLabel || "Retail Conviction Buying Peak Noise"}
          isNegative={cut.isNegative}
        />
      </div>

      <div
        style={{
          backgroundColor: VOX_COLORS.inkBlack,
          color: VOX_COLORS.paperWhite,
          padding: "18px 28px",
          borderLeft: `12px solid ${VOX_COLORS.hotRed}`,
          fontFamily: "'Courier New', Courier, monospace",
          fontSize: 24,
          fontWeight: 800,
          letterSpacing: "0.04em",
          transform: `scale(${stampSpring})`,
          opacity: stampSpring,
        }}
      >
        {cut.alertText || "⚠️ WARNING: INSTITUTIONAL SMART MONEY EXITING INTO RETAIL FOMO"}
      </div>

      <VoxCaptionOverlay
        text={cut.voiceoverText}
        durationSeconds={cut.durationSeconds || (cut.out_seconds - cut.in_seconds)}
      />
    </AbsoluteFill>
  );
};

// ============================================================================
// 2. CHART / DIVERGENCE SCENE: SPY 76% Divergence Signal
// ============================================================================
const VoxDivergenceChartScene: React.FC<{ cut: VoxSceneCut }> = ({ cut }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const lineProgress = spring({
    frame: frame - 6,
    fps,
    config: { damping: 16, stiffness: 85 },
  });

  const pinSpring = spring({
    frame: frame - 42,
    fps,
    config: { damping: 12, stiffness: 130 },
  });

  return (
    <AbsoluteFill style={{ padding: "80px 60px 170px", justifyContent: "space-between" }}>
      <div>
        <div style={{ marginBottom: 18 }}>
          <VoxAnnotationBadge figureNumber={cut.figureNumber} label={cut.figureLabel} />
        </div>
        <VoxHeadline title={cut.headline} subtitle={cut.subtitle} fontSize={72} />
      </div>

      <div
        style={{
          position: "relative",
          height: 500,
          border: `3px solid ${VOX_COLORS.inkBlack}`,
          backgroundColor: VOX_COLORS.paperWhite,
          boxShadow: `8px 8px 0px ${VOX_COLORS.hotRed}`,
          padding: 24,
          overflow: "hidden",
        }}
      >
        <Img
          src={resolveAsset("assets/archival_map.svg")}
          style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover", opacity: 0.35 }}
        />

        <svg viewBox="0 0 800 440" style={{ position: "absolute", inset: 20, width: "calc(100% - 40px)", height: "calc(100% - 40px)" }}>
          <line x1="40" y1="380" x2="760" y2="380" stroke={VOX_COLORS.inkBlack} strokeWidth="2" />
          <line x1="40" y1="40" x2="40" y2="380" stroke={VOX_COLORS.inkBlack} strokeWidth="2" />

          {/* Retail FOMO line (Red dashed line climbing to peak trap) */}
          <path
            d="M 60,320 Q 240,240 420,110 T 720,360"
            fill="none"
            stroke={VOX_COLORS.hotRed}
            strokeWidth="6"
            strokeDasharray="12 8"
            strokeDashoffset={interpolate(lineProgress, [0, 1], [600, 0])}
          />

          {/* CWT Consensus Exit Line (Solid Black line turning short early) */}
          <path
            d="M 60,320 Q 240,240 380,210 Q 520,290 720,330"
            fill="none"
            stroke={VOX_COLORS.inkBlack}
            strokeWidth="7"
            strokeDashoffset={interpolate(lineProgress, [0, 1], [600, 0])}
          />
        </svg>

        <div
          style={{
            position: "absolute",
            left: "48%",
            top: "20%",
            transform: `translate(-50%, -50%) scale(${pinSpring})`,
            opacity: pinSpring,
          }}
        >
          <Img src={resolveAsset("assets/map_pin.svg")} style={{ width: 64, height: 80 }} />
        </div>

        <div
          style={{
            position: "absolute",
            left: 50,
            bottom: 30,
            backgroundColor: VOX_COLORS.paperWhite,
            border: `2px solid ${VOX_COLORS.inkBlack}`,
            padding: "8px 16px",
            fontFamily: "'Courier New', monospace",
            fontSize: 20,
            fontWeight: 800,
          }}
        >
          ● CWT EXIT: 48H BEFORE DROP
        </div>

        <div
          style={{
            position: "absolute",
            right: 50,
            top: 30,
            backgroundColor: VOX_COLORS.hotRed,
            color: VOX_COLORS.paperWhite,
            padding: "8px 16px",
            fontFamily: "'Courier New', monospace",
            fontSize: 20,
            fontWeight: 800,
            transform: `scale(${pinSpring})`,
            opacity: pinSpring,
          }}
        >
          ▲ RETAIL TRAP PEAK (-3.8% DROP)
        </div>
      </div>

      <div style={{ display: "flex", justifyContent: "center" }}>
        <VoxStatHero
          targetValue={cut.statNumber || 76}
          suffix="%"
          label={cut.statLabel || "SPY Reversal Predictive Accuracy"}
        />
      </div>

      <VoxCaptionOverlay
        text={cut.voiceoverText}
        durationSeconds={cut.durationSeconds || (cut.out_seconds - cut.in_seconds)}
      />
    </AbsoluteFill>
  );
};

// ============================================================================
// 3. SOURCES RADAR SCENE: 16,420+ Sources Across YouTube, Reddit, FinTwit
// ============================================================================
const VoxSourcesRadarScene: React.FC<{ cut: VoxSceneCut }> = ({ cut }) => {
  return (
    <AbsoluteFill style={{ padding: "80px 60px 170px", justifyContent: "space-between" }}>
      <div>
        <div style={{ marginBottom: 18 }}>
          <VoxAnnotationBadge figureNumber={cut.figureNumber} label={cut.figureLabel} />
        </div>
        <VoxHeadline title={cut.headline} subtitle={cut.subtitle} fontSize={72} />
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 18, margin: "20px 0" }}>
        {[
          { name: "YouTube Financial Feeds", stat: "4,200 Channel Transcripts", badge: "Hype vs Reality" },
          { name: "Reddit (r/Daytrading, r/Options)", stat: "6,480 Sentiment Signals", badge: "Extreme FOMO Trap" },
          { name: "FinTwit & Financial Wires", stat: "5,740 Institutional Streams", badge: "Smart Conviction" },
        ].map((src, idx) => (
          <VoxCutout key={idx} delay={idx * 4} offsetColor={VOX_COLORS.hotRed} rotation={idx % 2 === 0 ? 0.8 : -0.8}>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "22px 32px",
                backgroundColor: VOX_COLORS.paperWhite,
              }}
            >
              <div>
                <div style={{ fontFamily: "Impact, sans-serif", fontSize: 32, color: VOX_COLORS.inkBlack }}>
                  {src.name}
                </div>
                <div style={{ fontFamily: "'Courier New', monospace", fontSize: 20, color: VOX_COLORS.mutedGray, marginTop: 4 }}>
                  {src.stat}
                </div>
              </div>
              <div
                style={{
                  backgroundColor: VOX_COLORS.mustard,
                  color: VOX_COLORS.inkBlack,
                  border: `2px solid ${VOX_COLORS.inkBlack}`,
                  padding: "6px 16px",
                  fontFamily: "'Courier New', monospace",
                  fontSize: 18,
                  fontWeight: 800,
                }}
              >
                {src.badge}
              </div>
            </div>
          </VoxCutout>
        ))}
      </div>

      <div style={{ display: "flex", justifyContent: "center" }}>
        <VoxStatHero
          targetValue={cut.statNumber || 16420}
          suffix="+"
          label={cut.statLabel || "Verified Market Predictions Distilled Daily"}
        />
      </div>

      <VoxCaptionOverlay
        text={cut.voiceoverText}
        durationSeconds={cut.durationSeconds || (cut.out_seconds - cut.in_seconds)}
      />
    </AbsoluteFill>
  );
};

// ============================================================================
// 4. FOUNDER / TRACK RECORD SCENE: Gilad Bar-Ilan & Pre-Defined Risk
// ============================================================================
const VoxFounderTrackRecordScene: React.FC<{ cut: VoxSceneCut }> = ({ cut }) => {
  return (
    <AbsoluteFill style={{ padding: "80px 60px 170px", justifyContent: "space-between" }}>
      <div>
        <div style={{ marginBottom: 18 }}>
          <VoxAnnotationBadge figureNumber={cut.figureNumber} label={cut.figureLabel} />
        </div>
        <VoxHeadline title={cut.headline} subtitle={cut.subtitle} fontSize={72} />
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 16, margin: "20px 0" }}>
        {[
          { label: "CONFIRMED ENTRY LEVEL", value: "$482.50", desc: "Breakout Divergence Zone", color: VOX_COLORS.inkBlack },
          { label: "UPSIDE PROFIT TARGET", value: "$488.20", desc: "Crowd Liquidity Exit", color: "#10B981" },
          { label: "STRICT INVALIDATION STOP", value: "$479.80", desc: "Defined 1:3 Risk to Reward", color: VOX_COLORS.hotRed },
        ].map((item, idx) => (
          <VoxCutout key={idx} delay={idx * 4} offsetColor={VOX_COLORS.hotRed}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "20px 32px", backgroundColor: VOX_COLORS.paperWhite }}>
              <div>
                <div style={{ fontFamily: "'Courier New', monospace", fontSize: 18, fontWeight: 800, color: item.color }}>
                  {item.label}
                </div>
                <div style={{ fontFamily: "Impact, sans-serif", fontSize: 40, color: VOX_COLORS.inkBlack, marginTop: 2 }}>
                  {item.value}
                </div>
              </div>
              <div style={{ fontFamily: "Inter, sans-serif", fontSize: 20, color: VOX_COLORS.mutedGray }}>
                {item.desc}
              </div>
            </div>
          </VoxCutout>
        ))}
      </div>

      <div style={{ display: "flex", justifyContent: "center" }}>
        <VoxStatHero
          targetValue={cut.statNumber || 25}
          suffix="+ Yrs"
          label={cut.statLabel || "Market Experience • Founder Gilad Bar-Ilan"}
        />
      </div>

      <VoxCaptionOverlay
        text={cut.voiceoverText}
        durationSeconds={cut.durationSeconds || (cut.out_seconds - cut.in_seconds)}
      />
    </AbsoluteFill>
  );
};

// ============================================================================
// 5. COMPARISON SCENE: Stop Being Exit Liquidity
// ============================================================================
const VoxComparisonCardsScene: React.FC<{ cut: VoxSceneCut }> = ({ cut }) => {
  return (
    <AbsoluteFill style={{ padding: "80px 60px 170px", justifyContent: "space-between" }}>
      <div>
        <div style={{ marginBottom: 18 }}>
          <VoxAnnotationBadge figureNumber={cut.figureNumber} label={cut.figureLabel} />
        </div>
        <VoxHeadline title={cut.headline} subtitle={cut.subtitle} fontSize={72} />
      </div>

      <div style={{ display: "flex", gap: 28, margin: "24px 0" }}>
        <div style={{ flex: 1 }}>
          <VoxCutout delay={4} offsetColor={VOX_COLORS.inkBlack} rotation={-1}>
            <div style={{ padding: "32px 26px", backgroundColor: VOX_COLORS.paperWhite, minHeight: 460 }}>
              <div style={{ fontFamily: "Impact, sans-serif", fontSize: 32, color: VOX_COLORS.hotRed }}>
                CHASING SOCIAL HYPE
              </div>
              <div style={{ height: 4, backgroundColor: VOX_COLORS.hotRed, margin: "12px 0 18px" }} />
              <ul style={{ fontFamily: "Inter, sans-serif", fontSize: 21, color: VOX_COLORS.inkBlack, lineHeight: 1.8, paddingLeft: 20 }}>
                <li>Late entries into peak FOMO</li>
                <li>Emotional revenge trading</li>
                <li>Used as exit liquidity</li>
                <li>No defined stop-loss risk</li>
              </ul>
            </div>
          </VoxCutout>
        </div>

        <div style={{ flex: 1 }}>
          <VoxCutout delay={10} offsetColor={VOX_COLORS.hotRed} rotation={1}>
            <div style={{ padding: "32px 26px", backgroundColor: VOX_COLORS.paperWhite, minHeight: 460 }}>
              <div style={{ fontFamily: "Impact, sans-serif", fontSize: 32, color: VOX_COLORS.inkBlack }}>
                TRADE THE REACTION
              </div>
              <div style={{ height: 4, backgroundColor: VOX_COLORS.hotRed, margin: "12px 0 18px" }} />
              <ul style={{ fontFamily: "Inter, sans-serif", fontSize: 21, color: VOX_COLORS.inkBlack, lineHeight: 1.8, paddingLeft: 20 }}>
                <li>Decisive consensus conviction</li>
                <li>Pre-calculated entry & target</li>
                <li>76% reversal predictive accuracy</li>
                <li>Capital protected before the drop</li>
              </ul>
            </div>
          </VoxCutout>
        </div>
      </div>

      <div
        style={{
          backgroundColor: VOX_COLORS.inkBlack,
          color: VOX_COLORS.paperWhite,
          padding: "18px 28px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontFamily: "'Courier New', monospace",
          fontSize: 22,
          fontWeight: 800,
          border: `3px solid ${VOX_COLORS.hotRed}`,
        }}
      >
        <span>DISCIPLINED EXECUTION</span>
        <span style={{ color: VOX_COLORS.mustard }}>STRICT 1:3 RISK/REWARD</span>
        <span style={{ color: VOX_COLORS.hotRed }}>ZERO FOMO</span>
      </div>

      <VoxCaptionOverlay
        text={cut.voiceoverText}
        durationSeconds={cut.durationSeconds || (cut.out_seconds - cut.in_seconds)}
      />
    </AbsoluteFill>
  );
};

// ============================================================================
// 6. CTA / OFFER SCENE: Get 20 Free Predictions
// ============================================================================
const VoxCtaOfferScene: React.FC<{ cut: VoxSceneCut }> = ({ cut }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pulseBtn = spring({
    frame: frame - 12,
    fps,
    config: { damping: 10, stiffness: 120 },
  });

  return (
    <AbsoluteFill style={{ padding: "80px 60px 170px", justifyContent: "space-between", textAlign: "center" }}>
      <div>
        <div style={{ display: "inline-block", marginBottom: 18 }}>
          <VoxAnnotationBadge figureNumber={cut.figureNumber} label={cut.figureLabel} />
        </div>
        <VoxHeadline title={cut.headline} subtitle={cut.subtitle} fontSize={78} align="center" />
      </div>

      <div style={{ margin: "24px 0" }}>
        <VoxCutout delay={4} offsetColor={VOX_COLORS.hotRed} rotation={0}>
          <div style={{ padding: "36px 44px", backgroundColor: VOX_COLORS.paperWhite, maxWidth: 840, margin: "0 auto" }}>
            <div style={{ fontFamily: "Impact, sans-serif", fontSize: 42, color: VOX_COLORS.inkBlack, textTransform: "uppercase" }}>
              FREE CROWD PREDICTION ACCESS
            </div>
            <div style={{ height: 4, backgroundColor: VOX_COLORS.hotRed, width: 220, margin: "14px auto 20px" }} />
            
            <div style={{ fontFamily: "Inter, sans-serif", fontSize: 24, color: VOX_COLORS.inkBlack, lineHeight: 1.7, textAlign: "left" }}>
              ✔ 20 Free Platform Prediction Credits Included<br />
              ✔ Real-Time Institutional Divergence Alerts<br />
              ✔ Top 5 Crowd Consensus Trade Ideas Weekly<br />
              ✔ No Credit Card Required to Start
            </div>
          </div>
        </VoxCutout>
      </div>

      <div style={{ transform: `scale(${pulseBtn})` }}>
        <div
          style={{
            display: "inline-block",
            backgroundColor: VOX_COLORS.hotRed,
            color: VOX_COLORS.paperWhite,
            padding: "22px 50px",
            fontFamily: "Impact, sans-serif",
            fontSize: 38,
            textTransform: "uppercase",
            letterSpacing: "0.05em",
            border: `4px solid ${VOX_COLORS.inkBlack}`,
            boxShadow: `8px 8px 0px ${VOX_COLORS.inkBlack}`,
          }}
        >
          START AT CROWDWISDOMTRADING.COM
        </div>
        <div
          style={{
            fontFamily: "'Courier New', monospace",
            fontSize: 22,
            color: VOX_COLORS.inkBlack,
            marginTop: 16,
            fontWeight: 800,
          }}
        >
          Collective Market Intelligence • 25+ Years Experience
        </div>
      </div>

      <VoxCaptionOverlay
        text={cut.voiceoverText}
        durationSeconds={cut.durationSeconds || (cut.out_seconds - cut.in_seconds)}
      />
    </AbsoluteFill>
  );
};

// ============================================================================
// MAIN COMPOSITION: VOX EXPLAINER WITH PER-SEQUENCE SYNCHRONIZED AUDIO
// ============================================================================
export const VoxExplainer: React.FC<VoxExplainerProps> = ({ cuts, audio }) => {
  const { fps } = useVideoConfig();

  return (
    <VoxBackground>
      {/* Each visual scene sequenced according to exact audio durations */}
      {cuts.map((cut) => {
        const from = Math.round(cut.in_seconds * fps);
        const duration = Math.max(15, Math.round((cut.out_seconds - cut.in_seconds) * fps));

        let sceneComponent: React.ReactNode = null;
        if (cut.visualType === "chart_divergence") {
          sceneComponent = <VoxDivergenceChartScene cut={cut} />;
        } else if (cut.visualType === "sources_radar") {
          sceneComponent = <VoxSourcesRadarScene cut={cut} />;
        } else if (cut.visualType === "founder_track_record") {
          sceneComponent = <VoxFounderTrackRecordScene cut={cut} />;
        } else if (cut.visualType === "comparison_cards") {
          sceneComponent = <VoxComparisonCardsScene cut={cut} />;
        } else if (cut.visualType === "cta_offer") {
          sceneComponent = <VoxCtaOfferScene cut={cut} />;
        } else {
          sceneComponent = <VoxHookStatScene cut={cut} />;
        }

        return (
          <Sequence key={cut.id} from={from} durationInFrames={duration}>
            {sceneComponent}
            {/* Per-sequence synchronized voiceover audio: starts on exact frame! */}
            {cut.audioSrc && (
              <Audio src={resolveAsset(cut.audioSrc)} volume={1.0} />
            )}
          </Sequence>
        );
      })}

      {/* Fallback Master Voiceover if cuts don't specify per-cut audio */}
      {audio?.narration?.src && !cuts.some((c) => c.audioSrc) && (
        <Audio src={resolveAsset(audio.narration.src)} volume={audio.narration.volume ?? 1.0} />
      )}

      {/* Subtle Background Music Bed (ducked to 0.12) */}
      {audio?.music?.src && (
        <Audio src={resolveAsset(audio.music.src)} volume={audio.music.volume ?? 0.12} loop />
      )}
    </VoxBackground>
  );
};
