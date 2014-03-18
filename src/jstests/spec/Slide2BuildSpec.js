describe("The slide deck class", function() {

    it("should find all matching slides in the container.", function() {
        deck = new SlideDeck(document.querySelector('#test_slides'));
        expect(deck.slides.length).toBe(2);
    });

    it("should exclude hidden slides", function() {
        deck = new SlideDeck(document.querySelector('#test_slides_with_hidden'));
        expect(document.querySelectorAll("#test_slides_with_hidden > slide").length)
            .toBe(3);
        expect(deck.slides.length).toBe(2);
    });

});

describe("build-item classes", function() {

    var deck;

    beforeEach(function() {
        deck = new SlideDeck(document.querySelector("#test_build_item"));
    });

    it("should mark build-item-* as to-build", function() {

        var build_items = deck.container.querySelectorAll("[class*='build-item']");

        // sanity check
        expect(build_items.length).toBe(4);

        // expect that to-build was added to each
        for (var j = 0, item; item = build_items[j]; ++j) {
            expect(item.classList.contains('to-build')).toBe(true);
        }

    });

    it("should show the first build-item on buildNext", function() {

        var build_item_1 = deck.container.querySelector('.build-item-1');

        expect(build_item_1.classList.contains('to-build')).toBeTruthy();
        deck.buildNextItem_();
        expect(build_item_1.classList.contains('to-build')).toBeFalsy();

    });

    it("should show items with the same index at the same time", function() {

        var build_item_2 = deck.container.querySelectorAll('.build-item-2');

        deck.buildNextItem_();
        deck.buildNextItem_();

        for (var j=0, item; item = build_item_2[j]; ++j) {
            expect(item.classList.contains('to-build')).toBeFalsy();
        }
    });

});

describe("mixed build-item classes and 'classic' build", function() {

    var deck;

    beforeEach(function() {
        deck = new SlideDeck(
            document.querySelector("#test_mixed_build_item_and_build")
        );
    });

    it("should build build-items first", function() {

        list = deck.container.querySelector('ul');
        items = list.querySelectorAll('li');
        for (var j=0, item; item = items[j]; ++j) {
            expect(item.classList.contains('to-build')).toBeTruthy();
        }

        deck.buildNextItem_();
        deck.buildNextItem_();

        for (var j=0, item; item = items[j]; ++j) {
            expect(item.classList.contains('to-build')).toBeTruthy();
        }

    });

});
