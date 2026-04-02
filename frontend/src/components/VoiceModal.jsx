import React, { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';

const VoiceModal = ({ isOpen, onClose, status, volume }) => {
    const canvasRef = useRef(null);
    const particles = useRef([]);
    const animationFrame = useRef(null);
    const volumeRef = useRef(0);

    useEffect(() => {
        volumeRef.current = volume;
    }, [volume]);

    useEffect(() => {
        if (!isOpen) return;

        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

        canvas.width = 400;
        canvas.height = 400;

        particles.current = [];
        const count = 500;
        for (let i = 0; i < count; i++) {
            particles.current.push({
                angle: Math.random() * Math.PI * 2,
                radius: Math.random() * 80,
                baseRadius: Math.random() * 80,
                speed: 0.002 + Math.random() * 0.006,
                size: Math.random() * 1.5 + 0.5,
                opacity: Math.random() * 0.7 + 0.1,
                noise: Math.random() * 100
            });
        }

        const animate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const centerX = canvas.width / 2;
            const centerY = canvas.height / 2;

            const currentVol = volumeRef.current;
            const volumeImpact = currentVol * 140;

            particles.current.forEach((p) => {
                p.angle += p.speed;

                const targetRadius = p.baseRadius + (volumeImpact * (p.baseRadius / 80));
                p.radius += (targetRadius - p.radius) * 0.1;

                const x = centerX + Math.cos(p.angle) * p.radius;
                const y = centerY + Math.sin(p.angle) * p.radius;

                ctx.fillStyle = `rgba(255, 255, 255, ${p.opacity})`;

                if (p.size > 1.2) {
                    ctx.shadowBlur = 6;
                    ctx.shadowColor = "rgba(255, 255, 255, 0.4)";
                } else {
                    ctx.shadowBlur = 0;
                }

                ctx.beginPath();
                ctx.arc(x, y, p.size, 0, Math.PI * 2);
                ctx.fill();
            });

            animationFrame.current = requestAnimationFrame(animate);
        };

        animate();
        return () => {
            if (animationFrame.current) {
                cancelAnimationFrame(animationFrame.current);
            }
        };
    }, [isOpen]);

    return (
        <AnimatePresence>
            {isOpen && (
                <motion.div
                    className="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 backdrop-blur-3xl"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                >
                    <div className="relative flex flex-col items-center gap-4 p-12 w-full h-full justify-center">
                        <button
                            onClick={onClose}
                            className="absolute top-8 right-8 p-4 text-white/30 hover:text-white transition-all hover:rotate-90 duration-300"
                        >
                            <X size={24} />
                        </button>

                        <div className="relative w-[400px] h-[400px] flex items-center justify-center pointer-events-none">
                            <canvas
                                ref={canvasRef}
                                className="w-full h-full"
                                width={400}
                                height={400}
                            />
                        </div>

                        <div className="flex flex-col items-center gap-1.5 mt-[-20px]">
                            <h2 className="text-lg font-normal text-white/80 tracking-wide font-sans text-center">
                                {status || "Say something..."}
                            </h2>
                            <p className="text-white/30 text-[10px] font-medium tracking-[0.3em] uppercase font-sans">
                                Neural Interface
                            </p>
                        </div>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
};

export default VoiceModal;
