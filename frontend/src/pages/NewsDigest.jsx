import { useEffect, useState } from "react";

export default function NewsDigest() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/news/latest")
      .then(res => res.json())
      .then(data => {
        setNews(data.articles || []);
        setLoading(false);
      });
  }, []);

  return (
    <div className="news-page">
      <h2>Tech News Digest</h2>

      {loading && <p>Loading latest news...</p>}

      {news.map((n, i) => (
        <div key={i} className="news-card">
          <h4>{n.title}</h4>
          <p>{n.source}</p>
          <a href={n.link} target="_blank" rel="noreferrer">
            Read more →
          </a>
        </div>
      ))}
    </div>
  );
}
