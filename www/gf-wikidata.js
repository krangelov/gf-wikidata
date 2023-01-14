function showSearches(searchbox) {
    if (searchbox.value.length < 3) return;

	const content = document.getElementById("content");
	fetch("https://www.wikidata.org/w/api.php?action=wbsearchentities&language="+content.dataset.lang+"&uselang="+content.dataset.lang+"&type=item&continue=0&origin=*&format=json&search="+encodeURIComponent(searchbox.value),
          { method: "GET" })
       .then((response) => response.json())
       .then((data) => {
                const searchResults = document.getElementById("searchResults");
                searchResults.innerHTML = "";
                searchResults.style.display = "none";
                for (const res of data.search) {
                    searchResults.style.display = "block";

                    const option = document.createElement("TR");
                    option.dataset.qid = res.id;
                    if (res.label != null) {
                        const value = document.createElement("DIV");
                        value.appendChild(document.createTextNode(res.label));
                        option.appendChild(value);
                    }
                    if (res.description != null) {
                        const descr = document.createElement("DIV");
                        descr.appendChild(document.createTextNode(res.description));
                        option.appendChild(descr);
                    }

                    option.addEventListener('mouseenter', (event) => {
                        let element = searchResults.firstElementChild;
                        while (element != null) {
                            element.className = null;
                            element = element.nextElementSibling;
                        }
                        event.target.className = "current";
                    });
                    option.addEventListener('mouseleave', (event) => {
                        let element = searchResults.firstElementChild;
                        while (element != null) {
                            element.className = null;
                            element = element.nextElementSibling;
                        }
                    });
                    option.addEventListener('click', (event) => {
                        loadEntity(event.target.parentElement.dataset.qid);
                    });

                    searchResults.appendChild(option);
                    
                    if (res.label == searchbox.value) {
                        searchbox.dataset.qid = res.id;
                    }
                }
             });
}

function searchInputOnKeyPress(event) {
    if (event.key === "Enter") {
        event.preventDefault();

        let element = searchResults.firstElementChild;
        while (element != null) {
            if (element.className == "current") {
                break;
            }
            element = element.nextElementSibling;
        }
        if (element == null)
            element = searchResults.firstElementChild;
        if (element != null) {
            loadEntity(element.dataset.qid);
        }
    }
}
function searchInputOnKeyDown(event) {
    const searchResults = document.getElementById("searchResults");
    if (event.code === "ArrowUp") {
        event.preventDefault();
        let element = searchResults.firstElementChild;
        let last    = null;
        while (element != null) {
            if (element.className == "current") {
                if (last != null) {
                    element.className = null;
                    last.className = "current";
                }
                break;
            }
            last    = element;
            element = element.nextElementSibling;
        }
    } else if (event.code === "ArrowDown") {
        event.preventDefault();
        let element = searchResults.firstElementChild;
        while (element != null) {
            const next = element.nextElementSibling;
            if (element.className == "current") {
                if (next != null) {
                    element.className = null;
                    next.className = "current";
                }
                break;
            }
            element = next;
        }
        if (element == null) {
            searchResults.firstElementChild.className = "current";
        }
    }
}
function loadEntity(qid) {
    const searchInput = document.getElementById("searchInput");
    searchInput.value = "";
    const searchResults = document.getElementById("searchResults");
    searchResults.style.display = "none";

    const content = document.getElementById("content");
    window.location.href = "index.wsgi?id="+qid+"&lang="+content.dataset.lang;
}

function init_editor() {
	let langs = window.localStorage.getItem('gp-languages');
	if (langs == null) {
		langs = []
	} else {
		langs = langs.split(' ');
	}

	let table = document.getElementById("from");
	let tr = table.lastElementChild.firstElementChild;
	while (tr != null) {
		var nameElem  = tr.firstElementChild.firstElementChild;
		var checkElem = tr.lastElementChild.firstElementChild;

		var name = nameElem.innerHTML;
		if (nameElem.tagName == "B" || langs.includes(name)) {
			checkElem.checked = true;
		}
		tr = tr.nextElementSibling;
	}
}

function select_language() {
	let langs = ""
	let table = document.getElementById("from");
	let tr = table.lastElementChild.firstElementChild;
	while (tr != null) {
		var nameElem  = tr.firstElementChild.firstElementChild;
		var checkElem = tr.lastElementChild.firstElementChild;

		var name = nameElem.innerHTML;
		if (checkElem.checked) {
			langs = langs + " " + name;
		}
		tr = tr.nextElementSibling;
	}

	window.localStorage.setItem('gp-languages', langs);
}

function edit_lex(span,event,lexical_id, lang) {
	if (span.classList.contains("selected-lexeme"))
		return;

	gfwordnet.selection = {langs_list: [], langs: {}}
	let table = document.getElementById("from");
	let tr = table.lastElementChild.firstElementChild;
	while (tr != null) {
		var nameElem  = tr.firstElementChild.firstElementChild;
		var checkElem = tr.lastElementChild.firstElementChild;

		var name = nameElem.innerHTML;
		if (checkElem.checked) {
			gfwordnet.selection.langs[checkElem.name] = {
				name:  name,
				index: gfwordnet.selection.langs_list.length+1
			}
			gfwordnet.selection.langs_list.push(checkElem.name);
		}
		tr = tr.nextElementSibling;
	}

	const result = node("table",{class:"result"},[
                     node("thead",{},[]),
                     node("tbody",{},[])
                   ]);
    const popup = node("div",{},[result]);
    document.body.appendChild(popup);

    span.classList.add("selected-lexeme");

    document.body.addEventListener("click", function closeFn(event) {
		let hit = (event.target == span);
		if (!hit) {
			let e = event.target;
			while (e != null) {
				if (e == popup) {
					hit = true;
					break;
				}
				e = e.parentElement;
			}
		}

		if (!hit) {
			popup.remove();
			span.classList.remove("selected-lexeme");
			document.body.removeEventListener("click",closeFn);
		}
	});

	const ctxt = {rows: gfwordnet.render_rows(result,gfwordnet.selection,true,[{lemma: lexical_id}])};
	const helper = function (senses) {
		gfwordnet.senses = senses; // save the result to be used for filtering
		gfwordnet.render_senses(ctxt,gfwordnet.selection,result,null,senses);
		setTimeout(function() {
			popup.style.position = "absolute";
			popup.style.top = span.offsetTop+span.offsetHeight-1;
			popup.style.left = span.offsetLeft;

			const offsetRight = span.offsetLeft + popup.offsetWidth;
			if (offsetRight > document.body.offsetWidth) {
				popup.style.left = span.offsetLeft - (offsetRight - document.body.offsetWidth);
			}
		})
	}
	gfwordnet.sense_call("lexical_ids="+encodeURIComponent(lexical_id),helper);
}
