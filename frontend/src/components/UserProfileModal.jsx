import React, { useState } from "react";
import {
  X,
  User,
  Mail,
  Phone,
  Linkedin,
  Github,
  Twitter,
  Trophy,
  GraduationCap,
  Edit3,
  Save,
  LogOut,
  ChevronLeft
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { motion, AnimatePresence } from "framer-motion";
import "../styles/profile-modal.css";

export default function UserProfileModal({ isOpen, onClose }) {
  const { user, logout } = useAuth();
  const [view, setView] = useState("display"); // "display" or "edit"

  React.useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => { document.body.style.overflow = ''; };
  }, [isOpen]);

  const [profile, setProfile] = useState({
    phone: "+91 98765 43210",
    linkedin: "https://linkedin.com/in/maargha-dev",
    github: "https://github.com/maargha-platform",
    twitter: "https://x.com/maargha_ai",
    leetcode: "https://leetcode.com/maargha_user",
    education: "Bachelor of Technology in Computer Science | AI & ML Specialization | Tier 1 Institution"
  });

  const [form, setForm] = useState(profile);

  const handleSave = () => {
    setProfile(form);
    setView("display");
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  if (!isOpen) return null;

  return (
    <div className="profile-modal-overlay">
      <motion.div
        className="profile-modal-backdrop"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
      />

      <motion.div
        className="profile-modal-content"
        initial={{ opacity: 0, scale: 0.9, y: 30 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.9, y: 30 }}
        transition={{ type: "spring", damping: 25, stiffness: 350 }}
      >
        <button className="profile-modal-close" onClick={onClose}>
          <X size={20} />
        </button>

        {/* Expansive Header */}
        <header className="profile-modal-header">
          <div className="modal-avatar-wrapper">
            <div className="modal-avatar">
              {user?.name?.charAt(0)?.toUpperCase() || "U"}
            </div>
          </div>
          <div className="modal-user-title">
            <h2>{user?.name || "Professional Identity"}</h2>
            <p className="flex items-center gap-2">
              <Mail size={16} className="opacity-50" />
              {user?.email || "Connect your digital identity"}
            </p>
          </div>
        </header>

        {/* Wide Content Area */}
        <div className="profile-modal-body" data-lenis-prevent>
          <AnimatePresence mode="wait">
            {view === "display" ? (
              <motion.div
                key="display"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="modal-info-grid"
              >
                <InfoItem icon={<Phone size={16} />} label="Phone" value={profile.phone} />
                <InfoItem icon={<Linkedin size={16} />} label="LinkedIn" value={profile.linkedin} />
                <InfoItem icon={<Github size={16} />} label="GitHub" value={profile.github} />
                <InfoItem icon={<Twitter size={16} />} label="Twitter / X" value={profile.twitter} />
                <InfoItem icon={<Trophy size={16} />} label="LeetCode" value={profile.leetcode} />
                <InfoItem icon={<GraduationCap size={16} />} label="Education" value={profile.education} wide />
              </motion.div>
            ) : (
              <motion.div
                key="edit"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
              >
                <div className="edit-header">
                  <button onClick={() => setView("display")} className="back-btn">
                    <ChevronLeft size={20} />
                  </button>
                  <h3 className="font-bold text-xl">Edit Profile</h3>
                </div>

                <div className="edit-grid">
                  <Input name="phone" value={form.phone} onChange={handleChange} label="Phone" />
                  <Input name="linkedin" value={form.linkedin} onChange={handleChange} label="LinkedIn" />
                  <Input name="github" value={form.github} onChange={handleChange} label="GitHub" />
                  <Input name="twitter" value={form.twitter} onChange={handleChange} label="Twitter / X" />
                  <div className="edit-grid-wide">
                    <Input name="leetcode" value={form.leetcode} onChange={handleChange} label="LeetCode" />
                  </div>
                  <div className="edit-grid-wide">
                    <TextArea name="education" value={form.education} onChange={handleChange} label="Education" />
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Fixed Footer */}
        <footer className="profile-modal-footer">
          <div className="modal-footer-actions">
            {view === "display" ? (
              <>
                <button className="modal-logout-btn" onClick={() => { logout(); onClose(); }} title="Terminate Session">
                  <LogOut size={20} />
                </button>
                <button className="modal-edit-btn flex items-center justify-center gap-2" onClick={() => setView("edit")}>
                  <Edit3 size={18} />
                  Edit Profile
                </button>
              </>
            ) : (
              <>
                <button className="px-6 py-3 rounded-xl border border-border hover:bg-secondary font-semibold transition-all text-sm" onClick={() => setView("display")}>
                  Cancel
                </button>
                <button className="modal-edit-btn flex items-center justify-center gap-2" onClick={handleSave}>
                  <Save size={18} />
                  Save Changes
                </button>
              </>
            )}
          </div>
        </footer>
      </motion.div>
    </div>
  );
}

const InfoItem = ({ icon, label, value, wide }) => (
  <div className={`modal-info-item ${wide ? 'wide' : ''}`}>
    <span className="info-label-sm">
      {icon}
      {label}
    </span>
    <span className="info-value-md">{value || "Unset"}</span>
  </div>
);

const Input = ({ label, name, value, onChange }) => (
  <div className="space-y-1">
    <label className="input-group-label">{label}</label>
    <input
      className="modal-input"
      name={name}
      value={value}
      onChange={onChange}
    />
  </div>
);

const TextArea = ({ label, name, value, onChange }) => (
  <div className="space-y-1">
    <label className="input-group-label">{label}</label>
    <textarea
      className="modal-input modal-textarea"
      name={name}
      value={value}
      onChange={onChange}
    />
  </div>
);
