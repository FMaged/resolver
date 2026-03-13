from src.cli import parser




args = parser.parse_args()

if args.file:
    print(f"FILE: {args.file}")
    # with open(args.file) as f:
    #     domains = [line.strip() for line in f if line.strip()]
elif args.domain:
    domains = args.domain
    print(f"DOMAIN: {domains}")
else:
    parser.error("You must provide domains either as arguments or with -f")