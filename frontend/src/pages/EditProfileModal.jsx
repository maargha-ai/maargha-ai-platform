import React, { useState } from "react";
import { motion } from "framer-motion";

export default function EditProfileModal({ profile, onClose, onSave }) {
  const [form, setForm] = useState(profile);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  return (
    <motion.div
      className="modal-backdrop"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <motion.div
        className="modal-card"
        initial={{ scale: 0.95, y: 20 }}
        animate={{ scale: 1, y: 0 }}
        exit={{ scale: 0.95, y: 20 }}
      >
        <h3>Edit Profile</h3>

        <div className="modal-form">
          <Input label="Phone" name="phone" value={form.phone} onChange={handleChange} />
          <Input label="LinkedIn" name="linkedin" value={form.linkedin} onChange={handleChange} />
          <Input label="GitHub" name="github" value={form.github} onChange={handleChange} />
          <Input label="X (Twitter)" name="twitter" value={form.twitter} onChange={handleChange} />
          <Input label="LeetCode" name="leetcode" value={form.leetcode} onChange={handleChange} />
          <Textarea label="Education" name="education" value={form.education} onChange={handleChange} />
        </div>

        <div className="modal-actions">
          <button className="ghost-btn" onClick={onClose}>Cancel</button>
          <button className="save-btn" onClick={() => onSave(form)}>Save Profile</button>
        </div>
      </motion.div>
    </motion.div>
  );
}

function Input({ label, ...props }) {
  return (
    <div className="field">
      <label>{label}</label>
      <input {...props} />
    </div>
  );
}

function Textarea({ label, ...props }) {
  return (
    <div className="field">
      <label>{label}</label>
      <textarea rows={3} {...props} />
    </div>
  );
}
