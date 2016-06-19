def add_positions(pos1, pos2):
    """
    Get a new Position where two positions are added.

    NOTE: Position is a two element tuple: (x, y)

    :param Position pos1
    :param Position pos2
    :return added Position
    :rtype Position
    """

    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


def offset_rect(offset, rect):
    """
    Get a new Rect where rect is translated by offset.

    NOTE: Rect is a tuple having following structure: ((left, top), (right, bottom))

    :param Position offset
    :param Rect rect
    :return translated Rect
    :rtype Rect
    """

    top_left, bottom_right = rect
    return add_positions(offset, top_left), add_positions(offset, bottom_right)


def bounding_box(rects):
    """
    Get a new Rect which circumscribes all the rects.

    :param list rects
    :return bounding Rect
    :rtype Rect
    """

    top = float('inf')
    left = float('inf')
    bottom = 0
    right = 0
    for rect in rects:
        top_left, bottom_right = rect
        top = min(top, top_left[1])
        left = min(left, top_left[0])
        bottom = max(bottom, bottom_right[1])
        right = max(right, bottom_right[0])

    return ((left, top), (right, bottom))


def padding_box(rect, padding):
    """
    Get a new Rect where rect is enlarged by padding width.

    :param Rect rect
    :param int padding
    :return enlarged Rect
    :rtype Rect
    """

    top_left, bottom_right = rect

    return (add_positions(top_left, (-padding, -padding)),
            add_positions(bottom_right, (padding, padding)))
