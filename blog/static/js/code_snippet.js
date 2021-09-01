

function createCodeSnippet(language, content) {
    return `
<div class="code-snippet">
<div class="code-snippet-header">
<span><i class="fa fa-code"></i> ${language}</span>
<button class="fa fa-copy" onclick="navigator.clipboard.writeText('${content}')"></button>
</div>
<div class="code-snippet-content">
<code>
    ${content}
</code>
</div>
</div>
`
}

class CodeSnippet {

    constructor(text, content, language) {
        this.text = text;
        this.content = content;
        this.language = language;
    }

    html() {
        return `
        <div class="code-snippet">
            <div class="code-snippet-header">
                <span><i class="fa fa-code"></i>${this.language}</span>
                <button class="fa fa-copy" onclick="navigator.clipboard.writeText('${this.text}')"></button>
            </div>
            <div class="code-snippet-content">
                <code>
                    ${this.content}
                </code>
            </div>
        </div>
        `
    }
}


$(document).ready(function () {
    $('pre').each(function() {
        let element = $(this);
        let language = 'Python';

        if (element.attr('language')) {
            language = element.attr('language');
        }

        let codeSnippet = new CodeSnippet(element.text(), element.html(), language.toUpperCase());
        element.replaceWith(codeSnippet.html());
    });
})
