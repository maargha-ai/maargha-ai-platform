import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useAuth } from "../context/AuthContext";
import EditProfileModal from "../pages/EditProfileModal";
import "../styles/userprofile.css";

export default function UserProfile() {
  const { user } = useAuth();

  const [profile, setProfile] = useState({
    phone: "+91 XXXXX XXXXX",
    linkedin: "https://linkedin.com/in/username",
    github: "https://github.com/username",
    twitter: "https://x.com/username",
    leetcode: "https://leetcode.com/username",
    education: "BTech Computer Science"
  });

  const [isEditing, setIsEditing] = useState(false);

  return (
    <div className="profile-page">
      <div className="profile-view-card">
        {/* Header */}
        <div className="profile-header">
          <div className="profile-avatar-lg">
            {user?.name?.charAt(0)?.toUpperCase() || "U"}
          </div>
          <div>
            <h2>{user?.name || "User Name"}</h2>
            <p className="username">@{user?.username || "username"}</p>
          </div>
        </div>

        {/* Info grid */}
        <div className="profile-info-grid">
          <Info label="Phone" value={profile.phone} />
          <Info label="LinkedIn" value={profile.linkedin} />
          <Info label="GitHub" value={profile.github} />
          <Info label="X (Twitter)" value={profile.twitter} />
          <Info label="LeetCode" value={profile.leetcode} />
          <Info label="Education" value={profile.education} wide />
        </div>

        {/* Actions */}
        <div className="profile-actions">
          <button className="edit-btn" onClick={() => setIsEditing(true)}>
            Edit Profile
          </button>
        </div>
      </div>

      {/* Edit Modal */}
      <AnimatePresence>
        {isEditing && (
          <EditProfileModal
            profile={profile}
            onClose={() => setIsEditing(false)}
            onSave={(updated) => {
              setProfile(updated);
              setIsEditing(false);
            }}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

function Info({ label, value, wide }) {
  return (
    <div className={`info-item ${wide ? "wide" : ""}`}>
      <span className="info-label">{label}</span>
      <span className="info-value">{value || "—"}</span>
    </div>
  );
}
