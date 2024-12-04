import React, { useEffect, useState } from "react";

interface UserStats {
  username: string;
  wins_count: number;
  w_l: number;
}

interface LeaderboardResponse {
  user_stats: UserStats;
  leaderboard_stats: UserStats[];
}

const Leaderboard: React.FC = () => {
  const [leaderboard, setLeaderboard] = useState<UserStats[]>([]);
  const [userStats, setUserStats] = useState<UserStats | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const response = await fetch("http://localhost:5002/leaderboard/?top_n=20", {
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("Failed to fetch leaderboard");
        }
        const data: LeaderboardResponse = await response.json();
        setUserStats(data.user_stats);
        setLeaderboard(data.leaderboard_stats);
        console.log(data)
      } catch (error) {
        console.error("Error fetching leaderboard:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) {    
    return <div className="leaderboard">Загрузка списка лидеров...</div>;
  }

  return (
    <div className="leaderboard">
      <h2>Список лидеров</h2>
      {userStats && (
        <div className="user-stats">
          <h3>Ваша статистика</h3>
          <p>Победы: {userStats.wins_count}</p>
          <p>Отношение W/L: {userStats.w_l}</p>
        </div>
      )}
      <table>
        <thead>
          <tr>
            <th>Место</th>
            <th>Имя пользователя</th>
            <th>Победы</th>
            <th>Отношение W/L</th>
          </tr>
        </thead>
        <tbody>
          {leaderboard.map((user, index) => (
            <tr key={user.username}>
              <td>{index + 1}</td>
              <td>{user.username}</td>
              <td>{user.wins_count}</td>
              <td>{user.w_l}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Leaderboard;
