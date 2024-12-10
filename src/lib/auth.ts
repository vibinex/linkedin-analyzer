import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import crypto from 'crypto';

export function generateState() {
	return crypto.randomBytes(32).toString('hex');
}

export async function getSession() {
	const cookieStore = await cookies();
	const sessionCookie = cookieStore.get('session');
	if (!sessionCookie) {
		return null;
	}

	try {
		return JSON.parse(sessionCookie.value);
	} catch {
		return null;
	}
}

export async function requireAuth() {
	const session = await getSession();
	if (!session) {
		redirect('/');
	}
	return session;
}