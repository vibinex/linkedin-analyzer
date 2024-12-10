'use client';

import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { format, subDays } from 'date-fns';

interface Session {
	user: {
		name: string;
		email: string;
		picture: string;
	};
	accessToken: string;
}

export default function Dashboard() {
	const [session, setSession] = useState<Session | null>(null);
	const [dateRange, setDateRange] = useState({
		start: format(subDays(new Date(), 30), 'yyyy-MM-dd'),
		end: format(new Date(), 'yyyy-MM-dd'),
	});

	useEffect(() => {
		// Check session on component mount
		fetch('/api/auth/session')
			.then(res => res.json())
			.then(data => {
				if (!data.session) {
					window.location.href = '/';
				} else {
					setSession(data.session);
				}
			})
			.catch(() => {
				window.location.href = '/';
			});
	}, []);

	// Mock data - will be replaced with real LinkedIn API data
	const data = [
		{
			name: 'Conversion Funnel',
			'Requests Sent': 100,
			'Accepted Connections': 65,
			'Active Conversations': 30,
		},
	];

	if (!session) {
		return null;
	}

	return (
		<div className="min-h-screen bg-gray-100 p-8">
			<div className="max-w-7xl mx-auto">
				<div className="flex justify-between items-center mb-8">
					<h1 className="text-3xl font-bold text-gray-900">LinkedIn Sales Analytics</h1>
					<div className="flex items-center gap-4">
						<img
							src={session.user.picture}
							alt={session.user.name}
							className="w-8 h-8 rounded-full"
						/>
						<span className="text-gray-700">{session.user.name}</span>
					</div>
				</div>

				<div className="bg-white rounded-lg shadow p-6 mb-8">
					<div className="grid grid-cols-2 gap-4 mb-6">
						<div>
							<label className="block text-sm font-medium text-gray-700">Start Date</label>
							<input
								type="date"
								value={dateRange.start}
								onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
								className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
							/>
						</div>
						<div>
							<label className="block text-sm font-medium text-gray-700">End Date</label>
							<input
								type="date"
								value={dateRange.end}
								onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
								className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
							/>
						</div>
					</div>
				</div>

				<div className="bg-white rounded-lg shadow p-6">
					<h2 className="text-xl font-semibold mb-4">Connection Funnel</h2>
					<div className="w-full overflow-x-auto">
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
					</div>
				</div>
			</div>
		</div>
	);
}