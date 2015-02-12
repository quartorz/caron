preamble = {
    'title': 'Test',
    'author': 'quarter',
}

with Document():
    make_title()

    with Section('section'):
        with SubSection('sub section 1'):
            with Environment('table', optional='htbp'):
                centering()
                caption('table test', label='table')
                with Environment('tabular', required='cc'):
                    line += 'a & b \\\\'
                    line += 'c & d '

        with SubSection('sub section 2'):
            with SourceCode('test.py'):
                pass

            with Itemize():
                item += 'a'
                item += 'b'