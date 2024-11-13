declare namespace App {
	interface Locals { }

	interface Platform {
		env: {
			d1db: iclr;
		};
		context: {
			waitUntil(promise: Promise<any>): void;
		};
		caches: CacheStorage & { default: Cache }
	}

	interface Session { }

	interface Stuff { }
}