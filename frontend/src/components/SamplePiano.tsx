import { useEffect, useState, useRef } from "react";
import { Piano, KeyboardShortcuts, MidiNumbers } from "react-piano";
import "react-piano/dist/styles.css";
import * as Tone from "tone";

type Props = {
  audioUrl: string;
};

export default function SamplePiano({ audioUrl }: Props) {
  const [buffer, setBuffer] = useState<Tone.ToneAudioBuffer | null>(null);

  const [containerWidth, setContainerWidth] = useState<number>(600);
  const containerRef = useRef<HTMLDivElement | null>(null);

  const firstNote = MidiNumbers.fromNote("C4");
  const lastNote = MidiNumbers.fromNote("C5");
  const keyboardShortcuts = KeyboardShortcuts.create({
    firstNote,
    lastNote,
    keyboardConfig: KeyboardShortcuts.HOME_ROW,
  });

  useEffect(() => {
    if (!containerRef.current) return;

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        if (entry.contentRect.width !== containerWidth) {
          setContainerWidth(Math.floor(entry.contentRect.width));
        }
      }
    });

    resizeObserver.observe(containerRef.current);
    return () => resizeObserver.disconnect();
  }, [containerWidth]);

  useEffect(() => {
    if (audioUrl) {
      const buffer = new Tone.ToneAudioBuffer({
        url: audioUrl,
        onload: () => {
          setBuffer(buffer);
        },
        onerror: (err) => {
          console.error("Buffer load error:", err);
        },
      });
    }
  }, [audioUrl]);

  const playNote = (midiNumber: number) => {
    if (!buffer) return;

    const gain = new Tone.Gain(0.2).toDestination(); // Adjust volume here

    const player = new Tone.Player({
      url: buffer,
      fadeIn: 0.01,
      fadeOut: 0.01,
    }).connect(gain);

    const baseMidi = 60; // Middle C
    const semitoneShift = midiNumber - baseMidi;
    player.playbackRate = Math.pow(2, semitoneShift / 12);
    player.start();
  };

  const clampedWidth = Math.max(300, Math.min(containerWidth, 700));

  return (
    <div ref={containerRef} className="w-full flex justify-center mt-6 px-4">
      <div className="mx-auto" style={{ width: clampedWidth }}>
        <Piano
          width={clampedWidth}
          noteRange={{ first: firstNote, last: lastNote }}
          playNote={playNote}
          stopNote={() => {}}
          keyboardShortcuts={keyboardShortcuts}
        />
      </div>
    </div>
  );
}
