interface User {
	name: string;
	email: string;
	picture: string;
}

export default function Header({ user }: { user: User }) {
	return (
		<header className="flex justify-between items-center mb-8">
			<h1 className="text-3xl font-bold text-gray-900">LinkedIn Sales Analytics</h1>
			<div className="flex items-center gap-4">
				<img
					src={user.picture}
					alt={user.name}
					className="w-8 h-8 rounded-full"
				/>
				<span className="text-gray-700">{user.name}</span>
			</div>
		</header>
	);
}