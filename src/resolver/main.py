from cli import parser




args = parser.parse_args()

print(args)
#server=None 
#if args.server and args.server.startswith("@"):
#    server=args.server[1:]
#    print(f"SERVER: {server}")
#    print(f"type: {args.type}")
#    print(f"Domain: {args.name}")
#
#else:
#    server="system_resolver"
#    print(f"args: {args}")
