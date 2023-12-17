# echo was chosen because escaping conflicting symbols like `1` or `@import` wasn't straight forward with heredoc
  $ echo "Usage: cleancss [options] <source-file ...>" >> cleancss-output.txt
  $ echo "Options:" >> cleancss-output.txt
  $ echo "  -b, --batch                    If enabled, optimizes input files one by one" >> cleancss-output.txt
  $ echo "                                 instead of joining them together" >> cleancss-output.txt
  $ echo "  -c, --compatibility [ie7|ie8]  Force compatibility mode (see Readme for" >> cleancss-output.txt
  $ echo "                                 advanced examples)" >> cleancss-output.txt
  $ echo "  -d, --debug                    Shows debug information (minification time &" >> cleancss-output.txt
  $ echo "                                 compression efficiency)" >> cleancss-output.txt
  $ echo "  -f, --format <options>         Controls output formatting, see examples below" >> cleancss-output.txt
  $ echo "  -h, --help                     display this help" >> cleancss-output.txt
  $ echo "  -o, --output [output-file]     Use [output-file] as output instead of STDOUT" >> cleancss-output.txt
  $ echo "  -O <n> [optimizations]         Turn on level <n> optimizations; optionally" >> cleancss-output.txt
  $ echo "                                 accepts a list of fine-grained options," >> cleancss-output.txt
  $ echo "                                 defaults to \`1\`, see examples below," >> cleancss-output.txt
  $ echo "                                 IMPORTANT: the prefix is O (a capital o" >> cleancss-output.txt
  $ echo "                                 letter), NOT a 0 (zero, a number)" >> cleancss-output.txt
  $ echo "  -v, --version                  output the version number" >> cleancss-output.txt
  $ echo "  --batch-suffix <suffix>        A suffix (without extension) appended to input" >> cleancss-output.txt
  $ echo "                                 file name when processing in batch mode" >> cleancss-output.txt
  $ echo "                                 (\`-min\` is the default) (default: \"-min\")" >> cleancss-output.txt
  $ echo "  --inline [rules]               Enables inlining for listed sources (defaults" >> cleancss-output.txt
  $ echo "                                 to \`local\`)" >> cleancss-output.txt
  $ echo "  --inline-timeout [seconds]     Per connection timeout when fetching remote" >> cleancss-output.txt
  $ echo "                                 stylesheets (defaults to 5 seconds)" >> cleancss-output.txt
  $ echo "  --input-source-map [file]      Specifies the path of the input source map" >> cleancss-output.txt
  $ echo "                                 file" >> cleancss-output.txt
  $ echo "  --remove-inlined-files         Remove files inlined in <source-file ...> or" >> cleancss-output.txt
  $ echo "                                 via \`@import\` statements" >> cleancss-output.txt
  $ echo "  --source-map                   Enables building input's source map" >> cleancss-output.txt
  $ echo "  --source-map-inline-sources    Enables inlining sources inside source maps" >> cleancss-output.txt
  $ echo "  --with-rebase                  Enable URLs rebasing" >> cleancss-output.txt
  $ echo "  --watch                        Runs CLI in watch mode" >> cleancss-output.txt
  $ echo >> cleancss-output.txt
  $ echo "Examples:" >> cleancss-output.txt
  $ echo >> cleancss-output.txt
  $ echo "  %> cleancss one.css" >> cleancss-output.txt
  $ echo "  %> cleancss -o one-min.css one.css" >> cleancss-output.txt
  $ echo "  %> cleancss -o merged-and-minified.css one.css two.css three.css" >> cleancss-output.txt
  $ echo "  %> cleancss one.css two.css three.css | gzip -9 -c > merged-minified-and-gzipped.css.gz" >> cleancss-output.txt
  $ echo >> cleancss-output.txt
  $ echo "Formatting options:" >> cleancss-output.txt
  $ echo "  %> cleancss --format beautify one.css" >> cleancss-output.txt
  $ echo "  %> cleancss --format keep-breaks one.css" >> cleancss-output.txt
  $ echo "  %> cleancss --format 'indentBy:1;indentWith:tab' one.css" >> cleancss-output.txt
  $ echo "  %> cleancss --format 'breaks:afterBlockBegins=on;spaces:aroundSelectorRelation=on' one.css" >> cleancss-output.txt
  $ echo "  %> cleancss --format 'breaks:afterBlockBegins=2;spaces:aroundSelectorRelation=on' one.css" >> cleancss-output.txt
  $ echo >> cleancss-output.txt
  $ echo "Level 0 optimizations:" >> cleancss-output.txt
  $ echo "  %> cleancss -O0 one.css" >> cleancss-output.txt
  $ echo >> cleancss-output.txt
  $ echo "Level 1 optimizations:" >> cleancss-output.txt
  $ echo "  %> cleancss -O1 one.css" >> cleancss-output.txt
  $ echo "  %> cleancss -O1 removeQuotes:off;roundingPrecision:4;specialComments:1 one.css" >> cleancss-output.txt
  $ echo "  %> cleancss -O1 all:off;specialComments:1 one.css" >> cleancss-output.txt
  $ echo >> cleancss-output.txt
  $ echo "Level 2 optimizations:" >> cleancss-output.txt
  $ echo "  %> cleancss -O2 one.css" >> cleancss-output.txt
  $ echo "  %> cleancss -O2 mergeMedia:off;restructureRules:off;mergeSemantically:on;mergeIntoShorthands:off one.css" >> cleancss-output.txt
  $ echo "  %> cleancss -O2 all:off;removeDuplicateRules:on one.css" >> cleancss-output.txt

  $ cat > cleancss << EOF
  > #!/bin/sh
  > cat cleancss-output.txt
  > EOF

  $ chmod u+x cleancss

  $ export PATH=`pwd`:$PATH

  $ cleancss
  Usage: cleancss [options] <source-file ...>
  Options:
    -b, --batch                    If enabled, optimizes input files one by one
                                   instead of joining them together
    -c, --compatibility [ie7|ie8]  Force compatibility mode (see Readme for
                                   advanced examples)
    -d, --debug                    Shows debug information (minification time &
                                   compression efficiency)
    -f, --format <options>         Controls output formatting, see examples below
    -h, --help                     display this help
    -o, --output [output-file]     Use [output-file] as output instead of STDOUT
    -O <n> [optimizations]         Turn on level <n> optimizations; optionally
                                   accepts a list of fine-grained options,
                                   defaults to `1`, see examples below,
                                   IMPORTANT: the prefix is O (a capital o
                                   letter), NOT a 0 (zero, a number)
    -v, --version                  output the version number
    --batch-suffix <suffix>        A suffix (without extension) appended to input
                                   file name when processing in batch mode
                                   (`-min` is the default) (default: "-min")
    --inline [rules]               Enables inlining for listed sources (defaults
                                   to `local`)
    --inline-timeout [seconds]     Per connection timeout when fetching remote
                                   stylesheets (defaults to 5 seconds)
    --input-source-map [file]      Specifies the path of the input source map
                                   file
    --remove-inlined-files         Remove files inlined in <source-file ...> or
                                   via `@import` statements
    --source-map                   Enables building input's source map
    --source-map-inline-sources    Enables inlining sources inside source maps
    --with-rebase                  Enable URLs rebasing
    --watch                        Runs CLI in watch mode
  
  Examples:
  
    %> cleancss one.css
    %> cleancss -o one-min.css one.css
    %> cleancss -o merged-and-minified.css one.css two.css three.css
    %> cleancss one.css two.css three.css | gzip -9 -c > merged-minified-and-gzipped.css.gz
  
  Formatting options:
    %> cleancss --format beautify one.css
    %> cleancss --format keep-breaks one.css
    %> cleancss --format 'indentBy:1;indentWith:tab' one.css
    %> cleancss --format 'breaks:afterBlockBegins=on;spaces:aroundSelectorRelation=on' one.css
    %> cleancss --format 'breaks:afterBlockBegins=2;spaces:aroundSelectorRelation=on' one.css
  
  Level 0 optimizations:
    %> cleancss -O0 one.css
  
  Level 1 optimizations:
    %> cleancss -O1 one.css
    %> cleancss -O1 removeQuotes:off;roundingPrecision:4;specialComments:1 one.css
    %> cleancss -O1 all:off;specialComments:1 one.css
  
  Level 2 optimizations:
    %> cleancss -O2 one.css
    %> cleancss -O2 mergeMedia:off;restructureRules:off;mergeSemantically:on;mergeIntoShorthands:off one.css
    %> cleancss -O2 all:off;removeDuplicateRules:on one.css
