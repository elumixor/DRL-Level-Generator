from unittest import TestCase

from serialization import DataTypesSize, to_int, ByteSerializable, to_bytes, to_float, to_string, Endianness, to_list, \
    SerializationException, to_list_int, to_list_float, to_string_list


class C(ByteSerializable):
    def __init__(self, int_v, float_v, str_v):
        self.int_v = int_v
        self.float_v = float_v
        self.str_v = str_v

    def __eq__(self, other):
        return self.str_v == other.str_v and self.int_v == other.int_v and self.float_v == other.float_v

    def to_bytes(self, endianness: Endianness = Endianness.Native) -> bytes:
        return to_bytes(self.int_v, endianness) + to_bytes(self.float_v, endianness) + to_bytes(self.str_v, endianness)

    def assign_from_bytes(self, bytes_value, start_index=0, endianness: Endianness = Endianness.Native):
        self.int_v = to_int(bytes_value, start_index, endianness)
        start_index += DataTypesSize.Int
        self.float_v = to_float(bytes_value, start_index, endianness)
        start_index += DataTypesSize.Float
        self.str_v, bytes_read = to_string(bytes_value, start_index, endianness)
        return DataTypesSize.Int + DataTypesSize.Float + bytes_read


class CustomClassTests(TestCase):
    def test_custom_class_is_correctly_equal(self):
        self.assertEqual(C(1, 2.0, "hello"), C(1, 2.0, "hello"))
        self.assertNotEqual(C(2, 2.0, "hello"), C(1, 2.0, "hello"))
        self.assertNotEqual(C(1, 3.0, "hello"), C(1, 2.0, "hello"))
        self.assertNotEqual(C(1, 2.0, "hdello"), C(1, 2.0, "hello"))


class SerializationTests(TestCase):
    def test_string_serialization(self):
        string = "hello with \0 inside string с утф-восемь ыё"
        b = to_bytes(string)
        res, bytes_read = to_string(b)
        self.assertEqual(string, res)
        self.assertEqual(bytes_read, DataTypesSize.Int + len(string.encode('utf-8')))

    def test_simple_float(self):
        self.assertEqual(5.0, to_float(to_bytes(5.0)))

    def test_simple_int(self):
        self.assertEqual(5, to_int(to_bytes(5)))

    def test_endianness(self):
        self.assertEqual(5.0, to_float(to_bytes(5.0, Endianness.Native), 0, Endianness.Native))
        self.assertEqual(5.0, to_float(to_bytes(5.0, Endianness.Big), 0, Endianness.Big))
        self.assertEqual(5.0, to_float(to_bytes(5.0, Endianness.Little), 0, Endianness.Little))

    def test_int_list_serialization(self):
        my_list = [1, 2, 3, 0, 9]
        self.assertEqual(my_list, my_list)

        def transformer(value, start_index, endianness):
            return to_int(value, start_index, endianness), DataTypesSize.Int

        serialized, total_bytes = to_list(to_bytes(my_list), transformer)
        self.assertEqual(my_list, serialized)
        self.assertEqual(total_bytes, len(my_list) * DataTypesSize.Int + DataTypesSize.Int)

        serialized, total_bytes = to_list_int(to_bytes(my_list))
        self.assertEqual(my_list, serialized)

    def test_float_list_serialization(self):
        my_list = [1.0, 2.0, 3.05]

        self.assertEqual(my_list, my_list)

        def transformer(value, start_index, endianness):
            return to_float(value, start_index, endianness), DataTypesSize.Int

        serialized, total_bytes = to_list(to_bytes(my_list), transformer)
        self.assertEqual(len(my_list), len(serialized))
        self.assertEqual(total_bytes, len(my_list) * DataTypesSize.Float + DataTypesSize.Int)

        # float has 7 decimal digits of precision
        for i in range(len(my_list)):
            self.assertAlmostEqual(my_list[i], serialized[i], 7)

        serialized, total_bytes = to_list_float(to_bytes(my_list))
        self.assertEqual(len(my_list), len(serialized))
        self.assertEqual(total_bytes, len(my_list) * DataTypesSize.Float + DataTypesSize.Int)

        # float has 7 decimal digits of precision
        for i in range(len(my_list)):
            self.assertAlmostEqual(my_list[i], serialized[i], 7)

    def test_string_list_serialization(self):
        my_list = ["one", "two", "hello world \0", "min\0max"]

        self.assertEqual(my_list, my_list)

        def transformer(value, start_index, endianness):
            string, bytes_read = to_string(value, start_index)
            return string, bytes_read

        serialized, total_bytes = to_list(to_bytes(my_list), transformer)
        self.assertEqual(my_list, serialized)

        serialized, total_bytes = to_string_list(to_bytes(my_list))
        self.assertEqual(my_list, serialized)

    def test_empty_list_serialization(self):
        my_list = []

        self.assertEqual(my_list, my_list)

        serialized, total_bytes = to_list(to_bytes(my_list), lambda: None)
        self.assertEqual(len(my_list), len(serialized))

    def test_custom_class_serialization(self):
        instance = C(1, 2.0, "hello")
        other = C(2, 3.0, "hey")

        self.assertNotEqual(instance, other)

        serialized_bytes = to_bytes(instance)

        bytes_count = other.assign_from_bytes(serialized_bytes)

        self.assertEqual(instance, other)
        self.assertEqual(bytes_count, DataTypesSize.Int + DataTypesSize.Float + DataTypesSize.Int + len("hello"))

    def test_custom_class_list_serialization(self):
        my_list = [C(1, 2.0, "3.0"), C(2, 3.0, "4.0")]

        self.assertEqual(my_list, my_list)

        def transformer(value, start_index, endianness):
            string, bytes_read = to_string(value, start_index, endianness)
            return string, bytes_read

        serialized, total_bytes = to_list(to_bytes(my_list), transformer)
        self.assertEqual(len(my_list), len(serialized))

    def test_unserializable_class(self):
        class C2:
            pass

        self.assertRaises(SerializationException, lambda: to_bytes(C2()))

    def test_unserializable_list(self):
        class C2:
            pass

        self.assertRaises(SerializationException, lambda: to_bytes([C2()]))
