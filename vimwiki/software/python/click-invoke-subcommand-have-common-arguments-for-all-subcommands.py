= Invoke a click subcommand - Have all subcommands share a list of arguments =

{{{python
  DEFAULT_SUBCOMMAND = "p2n"


class CliState:
    def __init__(self):
        crawl_page: Optional[str] = None  # type: ignore


pass_state = click.make_pass_decorator(CliState, ensure=True)


def crawl_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(CliState)
        state.crawl_page = value
        return value

    return click.option(
        "-c",
        "--crawl",
        required=True,
        expose_value=False,
        help="Page in which to search in and find links for cards",
        callback=callback,
    )(f)


def common_options(f):
    f = crawl_option(f)
    return f


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    mode = ctx.invoked_subcommand if ctx.invoked_subcommand is not None else DEFAULT_SUBCOMMAND
    click.echo(f"Using mode: {mode}...")


# P2N -----------------------------------------------------------------------------------------

@main.command()
@common_options
@pass_state
def p2n(state):
    """Picture -> Name subcommand."""
    click.echo("Creating Picture -> Name cards...")
    # TODO ensure that I have pages to crawl...
    pages = find_pages()
    print("pages: ", pages)
    for page in pages:
        create_card_for(page)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
}}}
