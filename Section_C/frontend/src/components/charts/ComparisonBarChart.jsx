import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export default function ComparisonBarChart({ data, title, color = "#0f766e" }) {
  if (!data.length) {
    return (
      <section className="panel">
        <h3>{title}</h3>
        <p className="empty-state">No comparison data for the current filters.</p>
      </section>
    );
  }

  return (
    <section className="panel">
      <h3>{title}</h3>
      <div className="chart-wrapper">
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="label" angle={-25} textAnchor="end" interval={0} height={80} />
            <YAxis />
            <Tooltip />
            <Bar dataKey="avgMortality" fill={color} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
