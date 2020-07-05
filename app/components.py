import cable


@cable.component_view
def counter(state):
    count = state.get('count', 0)

    def inc():
        count += 1

    def dec():
        count -= 1

    return 'components/counter.html', {'count': count, 'inc': inc, 'dec': dec}
