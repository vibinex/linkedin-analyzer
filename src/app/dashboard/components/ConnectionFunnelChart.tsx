import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

export default function ConnectionFunnelChart({ data }: { data: any[] }) {
	return (
		<section className="bg-white rounded-lg shadow p-6">
			<h2 className="text-xl font-semibold mb-4">Connection Funnel</h2>
			<BarChart width={600} height={300} data={data}>
				<CartesianGrid strokeDasharray="3 3" />
				<XAxis dataKey="name" />
				<YAxis />
				<Tooltip />
				<Legend />
				<Bar dataKey="Requests Sent" fill="#8884d8" />
				<Bar dataKey="Accepted Connections" fill="#82ca9d" />
				<Bar dataKey="Active Conversations" fill="#ffc658" />
			</BarChart>
		</section>
	);
}