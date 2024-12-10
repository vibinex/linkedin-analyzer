export default function DateRangeSelector({ dateRange, setDateRange }: { dateRange: { start: string; end: string }; setDateRange: React.Dispatch<React.SetStateAction<{ start: string; end: string }>> }) {
	return (
		<section className="bg-white rounded-lg shadow p-6 mb-8">
			<div className="grid grid-cols-2 gap-4">
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
		</section>
	);
}