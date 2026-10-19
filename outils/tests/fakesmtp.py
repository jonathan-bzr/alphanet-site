import asyncio, sys, base64
out = sys.argv[1]
async def handle(r, w):
    w.write(b'220 fake ESMTP\r\n'); await w.drain()
    data_mode = False; buf = []
    while True:
        line = await r.readline()
        if not line: break
        if data_mode:
            if line == b'.\r\n':
                open(out, 'wb').write(b''.join(buf)); data_mode = False
                w.write(b'250 queued\r\n'); await w.drain(); continue
            buf.append(line); continue
        cmd = line.decode().strip()
        print('C:', cmd[:80], flush=True)
        if cmd.startswith('EHLO'): w.write(b'250-fake\r\n250-AUTH PLAIN LOGIN\r\n250 8BITMIME\r\n')
        elif cmd.startswith('AUTH PLAIN'):
            creds = base64.b64decode(cmd.split()[2]).split(b'\0')
            w.write(b'235 ok\r\n' if creds[2] == b'secret-test' else b'535 bad\r\n')
        elif cmd.startswith(('MAIL', 'RCPT')): w.write(b'250 ok\r\n')
        elif cmd == 'DATA': data_mode = True; w.write(b'354 go\r\n')
        elif cmd == 'QUIT': w.write(b'221 bye\r\n'); await w.drain(); break
        else: w.write(b'500 ?\r\n')
        await w.drain()
    w.close()
async def main():
    s = await asyncio.start_server(handle, '127.0.0.1', 2525)
    async with s: await s.serve_forever()
asyncio.run(main())
