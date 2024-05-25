/**
 * WEBSITE: https://themefisher.com
 * TWITTER: https://twitter.com/themefisher
 * FACEBOOK: https://www.facebook.com/themefisher
 * GITHUB: https://github.com/themefisher/
 */

(function ($) {
	'use strict';

	// Preloader js    
	$(window).on('load', function () {
		$('.preloader').fadeOut(100);
	});


	// navfixed
	$(window).scroll(function () {
		if ($('.navigation').offset().top > 50) {
			$('.navigation').addClass('nav-bg');
		} else {
			$('.navigation').removeClass('nav-bg');
		}
	});

	// masonry
	$('.masonry-wrapper').masonry({
		columnWidth: 1
	});

	// clipboard
	var clipInit = false;
	$('code').each(function () {
		var code = $(this),
			text = code.text();
		if (text.length > 2) {
			if (!clipInit) {
				var text, clip = new ClipboardJS('.copy-to-clipboard', {
					text: function (trigger) {
						text = $(trigger).prev('code').text();
						return text.replace(/^\$\s/gm, '');
					}
				});
				clipInit = true;
			}
			code.after('<span class="copy-to-clipboard">copy</span>');
		}
	});
	$('.copy-to-clipboard').click(function () {
		$(this).html('copied');
	});


	// match height
	$(function () {
		$('.match-height').matchHeight({
			byRow: true,
			property: 'height',
			target: null,
			remove: false
		});
	});

	// search
	$('#search-by').keyup(function () {
		if (this.value) {
			$(this).addClass('active')
		} else {
			$(this).removeClass('active')
		}
	})

	// Accordions
	$('.collapse').on('shown.bs.collapse', function () {
		$(this).parent().find('.ti-plus').removeClass('ti-plus').addClass('ti-minus');
	}).on('hidden.bs.collapse', function () {
		$(this).parent().find('.ti-minus').removeClass('ti-minus').addClass('ti-plus');
	});

})(jQuery);

const words = ["Insights", "World", "Typewriter", "Effect"];
let wordIndex = 0;
const typewriterText = document.getElementById("typewriter-text");

function typeWord(word, callback) {
    let i = 0;
    function type() {
        if (i < word.length) {
            typewriterText.textContent += word.charAt(i);
            i++;
            setTimeout(type, 150);
        } else {
            setTimeout(callback, 1000); // Wait before starting to delete
        }
    }
    type();
}

function deleteWord(callback) {
    let word = typewriterText.textContent;
    let i = word.length;
    function del() {
        if (i > 0) {
            typewriterText.textContent = word.substring(0, i - 1);
            i--;
            setTimeout(del, 100);
        } else {
            setTimeout(callback, 500); // Wait before starting to type the next word
        }
    }
    del();
}

function cycleWords() {
    typeWord(words[wordIndex], function() {
        deleteWord(function() {
            wordIndex = (wordIndex + 1) % words.length;
            cycleWords();
        });
    });
}

cycleWords();
