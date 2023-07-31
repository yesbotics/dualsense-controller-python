"""
This file uses code taken from the hidapi-cffi repo of the GitHub user Flok (https://github.com/flok/hidapi-cffi)

It is a modified version of hidapi-cffi from Johannes Baiter (https://github.com/jbaiter/hidapi-cffi)

License: See LICENSE.txt in this directory.

"""



from cffi import FFI
from sys import platform
ffi = FFI()

if platform.startswith('linux') or platform.startswith('darwin'):
    ffi.cdef("""

struct hid_device_;
typedef struct hid_device_ hid_device;

struct hid_device_info {
    char *path;
    unsigned short vendor_id;
    unsigned short product_id;
    wchar_t *serial_number;
    unsigned short release_number;
    wchar_t *manufacturer_string;
    wchar_t *product_string;
    unsigned short usage_page;
    unsigned short usage;
    int interface_number;
    struct hid_device_info *next;
};

int  hid_init(void);
int  hid_exit(void);

struct hid_device_info* hid_enumerate(unsigned short vendor_id,
                                      unsigned short product_id);
void hid_free_enumeration(struct hid_device_info *devs);
hid_device* hid_open(unsigned short vendor_id, unsigned short product_id,
                     const wchar_t *serial_number);
hid_device* hid_open_path(const char *path);
int hid_write(hid_device *device, const unsigned char *data, size_t length);
int hid_read_timeout(hid_device *dev, unsigned char *data, size_t length,
                     int milliseconds);
int hid_read(hid_device *device, unsigned char *data, size_t length);
int hid_set_nonblocking(hid_device *device, int nonblock);
int hid_send_feature_report(hid_device *device, const unsigned char *data,
                            size_t length);
int hid_get_feature_report(hid_device *device, unsigned char *data,
                           size_t length);
void hid_close(hid_device *device);
int hid_get_manufacturer_string(hid_device *device, wchar_t *string,
                                size_t maxlen);
int hid_get_product_string(hid_device *device, wchar_t *string,
                           size_t maxlen);
int hid_get_serial_number_string(hid_device *device, wchar_t *string,
                                 size_t maxlen);
int hid_get_indexed_string(hid_device *device, int string_index,
                           wchar_t *string, size_t maxlen);
const wchar_t* hid_error(hid_device *device);
""")
elif platform.startswith('win32'):
    ffi.cdef("""

typedef struct _OVERLAPPED {
    ULONG_PTR Internal;
    ULONG_PTR InternalHigh;
    union {
        struct {
            DWORD Offset;
            DWORD OffsetHigh;
        } DUMMYSTRUCTNAME;
        PVOID Pointer;
    } DUMMYUNIONNAME;

    HANDLE  hEvent;
} OVERLAPPED, *LPOVERLAPPED;

struct hid_device_ {
		HANDLE device_handle;
		BOOL blocking;
		USHORT output_report_length;
		size_t input_report_length;
		USHORT feature_report_length;
		unsigned char *feature_buf;
		void *last_error_str;
		DWORD last_error_num;
		BOOL read_pending;
		char *read_buf;
		OVERLAPPED ol;
		OVERLAPPED write_ol;
};

struct hid_device_;
typedef struct hid_device_ hid_device;

struct hid_device_info {
    char *path;
    unsigned short vendor_id;
    unsigned short product_id;
    wchar_t *serial_number;
    unsigned short release_number;
    wchar_t *manufacturer_string;
    wchar_t *product_string;
    unsigned short usage_page;
    unsigned short usage;
    int interface_number;
    struct hid_device_info *next;
};

int  hid_init(void);
int  hid_exit(void);

struct hid_device_info* hid_enumerate(unsigned short vendor_id,
                                      unsigned short product_id);
void hid_free_enumeration(struct hid_device_info *devs);
hid_device* hid_open(unsigned short vendor_id, unsigned short product_id,
                     const wchar_t *serial_number);
hid_device* hid_open_path(const char *path);
int hid_write(hid_device *device, const unsigned char *data, size_t length);
int hid_read_timeout(hid_device *dev, unsigned char *data, size_t length,
                     int milliseconds);
int hid_read(hid_device *device, unsigned char *data, size_t length);
int hid_set_nonblocking(hid_device *device, int nonblock);
int hid_send_feature_report(hid_device *device, const unsigned char *data,
                            size_t length);
int hid_get_feature_report(hid_device *device, unsigned char *data,
                           size_t length);
void hid_close(hid_device *device);
int hid_get_manufacturer_string(hid_device *device, wchar_t *string,
                                size_t maxlen);
int hid_get_product_string(hid_device *device, wchar_t *string,
                           size_t maxlen);
int hid_get_serial_number_string(hid_device *device, wchar_t *string,
                                 size_t maxlen);
int hid_get_indexed_string(hid_device *device, int string_index,
                           wchar_t *string, size_t maxlen);
const wchar_t* hid_error(hid_device *device);
""")
else:
    raise OSError('System platform not supported')

library_paths = (
    'libhidapi-hidraw.so',
    'libhidapi-hidraw.so.0',
    'libhidapi-libusb.so',
    'libhidapi-libusb.so.0',
    'libhidapi-iohidmanager.so',
    'libhidapi-iohidmanager.so.0',
    'libhidapi.dylib',
    'hidapi.dll',
    'libhidapi-0.dll'
)

for lib in library_paths:
    try:
        hidapi = ffi.dlopen(lib)
        break
    except OSError:
        pass
else:
    raise OSError("Could not find any hidapi library")

if hidapi.hid_init() == -1:
    raise OSError("Failed to initialize hidapi")


class DeviceInfo(object):
    __slots__ = ['path', 'vendor_id', 'product_id', 'serial_number',
                 'release_number', 'manufacturer_string', 'product_string',
                 'usage_page', 'usage', 'interface_number']

    def __init__(self, info_struct):
        #: Platform-specific device path
        self.path = ffi.string(info_struct.path)
        #: Device Vendor ID
        self.vendor_id = info_struct.vendor_id
        #: Device Product ID
        self.product_id = info_struct.product_id
        #: Serial Number
        self.serial_number = (ffi.string(info_struct.serial_number)
                              if info_struct.serial_number else None)
        #: Device Release Number in binary-coded decimal, also known as
        #  Device Version Number
        self.release_number = info_struct.release_number
        #: Manufacturer String
        self.manufacturer_string = (ffi.string(info_struct.manufacturer_string)
                                    if info_struct.manufacturer_string
                                    else None)
        #: Product string
        self.product_string = (ffi.string(info_struct.product_string)
                               if info_struct.product_string else None)
        #: Usage Page for this Device/Interface (Windows/Mac only).
        self.usage_page = info_struct.usage_page or None
        #: Usage for this Device/Interface (Windows/Mac only).
        self.usage = info_struct.usage or None
        #: The USB interface which this logical device represents. Valid on
        #  both Linux implementations in all cases, and valid on the Windows
        #  implementation only if the device contains more than one interface.
        self.interface_number = info_struct.interface_number


def enumerate(vendor_id=0, product_id=0):
    """ Enumerate the HID Devices.

    Returns a generator that yields all of the HID devices attached to the
    system.

    :param vendor_id:   Only return devices which match this vendor id
    :type vendor_id:    int
    :param product_id:  Only return devices which match this product id
    :type product_id:   int
    :return:            Generator that yields informations about attached
                        HID devices
    :rval:              generator(DeviceInfo)

    """
    devices = []
    info = hidapi.hid_enumerate(vendor_id, product_id)
    while info:
        devices.append(DeviceInfo(info))
        info = info.next
    hidapi.hid_free_enumeration(info)
    return devices


class Device(object):
    def __init__(self, info=None, path=None, vendor_id=None, product_id=None,
                 serial_number=None, blocking=True):
        """ Open a connection to a HID device.
        This can be done either from a DeviceInfo object, a device path or
        a combination of vendor id, product id and an optional serial number.
        If no serial number is passed, the first matching device will be
        selected.
        By setting :param blocking: to True, all reads will be blocking by
        default, otherwise they will return `None` if no data is available.

        :param info:        Information about the device to initialize
        :type info:         DeviceInfo
        :param path:        Platform-specific path to the device (e.g.
                            `/dev/hidraw0` on Linux)
        :type path:         str
        :param vendor_id:   Vendor ID
        :type vendor_id:    int
        :param product_id:  Product ID
        :type product_id:   int
        :param serial_number: Device serial number
        :type serial_number: str
        :param blocking:    Enable blocking reads by default
        :type blocking:     boolean

        """
        if info is not None:
            self._device = hidapi.hid_open_path(info.path)
        elif path is not None:
            self._device = hidapi.hid_open_path(path)
        elif not (vendor_id is None or product_id is None):
            self._device = hidapi.hid_open(vendor_id, product_id,
                                           serial_number or ffi.NULL)
        else:
            raise ValueError("Must provide either a DeviceInfo object, 'path' "
                             "or 'vendor_id' and 'product_id'.")
        if self._device == ffi.NULL:
            raise IOError("Could not open connection to device.")
        if not blocking:
            hidapi.hid_set_nonblocking(self._device, 1)

    def __del__(self):
        if self._device is not None:
            self.close()

    def write(self, data):
        """ Write an Output report to a HID device.

        :param data:        The data to be sent
        :type data:         str/bytes

        """
        self._check_device_status()
        bufp = ffi.new("unsigned char[]", len(data))
        buf = ffi.buffer(bufp, len(data))
        buf[0:] = data
        rv = hidapi.hid_write(self._device, bufp, len(data))
        if rv == -1:
            raise IOError("Failed to write to HID device.")

    def read(self, length, timeout_ms=0, blocking=False):
        """ Read an Input report from a HID device with timeout.

        Input reports are returned to the host through the `INTERRUPT IN`
        endpoint. The first byte will contain the Report number if the device
        uses numbered reports.
        By default reads are non-blocking, i.e. the method will return
        `None` if no data was available. Blocking reads can be enabled with
        :param blocking:. Additionally, a timeout for the read can be
        specified.

        :param length:      The number of bytes to read. For devices with
                            multiple reports, make sure to read an extra byte
                            for the report number.
        :param timeout_ms:  Timeout in miliseconds
        :type timeout_ms:   int
        :param blocking:    Block until data is available

        """
        self._check_device_status()
        bufp = ffi.new("unsigned char[]", length)
        if not timeout_ms and blocking:
            timeout_ms = -1
        if timeout_ms:
            rv = hidapi.hid_read_timeout(self._device, bufp, length,
                                         timeout_ms)
        else:
            rv = hidapi.hid_read(self._device, bufp, length)
        if rv == -1:
            raise IOError("Failed to read from HID device: {0}"
                          .format(self._get_last_error_string()))
        elif rv == 0:
            return None
        else:
            return ffi.buffer(bufp, rv)[:]

    def get_manufacturer_string(self):
        """ Get the Manufacturer String from the HID device.

        :return:    The Manufacturer String
        :rtype:     unicode

        """
        self._check_device_status()
        str_p = ffi.new("wchar_t[]", 255)
        rv = hidapi.hid_get_manufacturer_string(self._device, str_p, 255)
        if rv == -1:
            raise IOError("Failed to read manufacturer string from HID "
                          "device: {0}".format(self._get_last_error_string()))
        return ffi.string(str_p)

    def get_product_string(self):
        """ Get the Product String from the HID device.

        :return:    The Product String
        :rtype:     unicode

        """
        self._check_device_status()
        str_p = ffi.new("wchar_t[]", 255)
        rv = hidapi.hid_get_product_string(self._device, str_p, 255)
        if rv == -1:
            raise IOError("Failed to read product string from HID device: {0}"
                          .format(self._get_last_error_string()))
        return ffi.string(str_p)

    def get_serial_number_string(self):
        """ Get the Serial Number String from the HID device.

        :return:    The Serial Number String
        :rtype:     unicode

        """
        self._check_device_status()
        str_p = ffi.new("wchar_t[]", 255)
        rv = hidapi.hid_get_serial_number_string(self._device, str_p, 255)
        if rv == -1:
            raise IOError("Failed to read serial number string from HID "
                          "device: {0}".format(self._get_last_error_string()))
        return ffi.string(str_p)

    def send_feature_report(self, data, report_id=0x0):
        """ Send a Feature report to the device.

        Feature reports are sent over the Control endpoint as a Set_Report
        transfer.

        :param data:        The data to send
        :type data:         str/bytes
        :param report_id:   The Report ID to send to
        :type report_id:    int

        """
        self._check_device_status()
        bufp = ffi.new("unsigned char[]", len(data)+1)
        buf = ffi.buffer(bufp, len(data)+1)
        buf[0] = report_id
        buf[1:] = data
        rv = hidapi.hid_send_feature_report(self._device, bufp, len(bufp))
        if rv == -1:
            raise IOError("Failed to send feature report to HID device: {0}"
                          .format(self._get_last_error_string()))

    def get_feature_report(self, report_id, length):
        """ Get a feature report from the device.

        :param report_id:   The Report ID of the report to be read
        :type report_id:    int
        :return:            The report data
        :rtype:             str/bytes

        """
        self._check_device_status()
        bufp = ffi.new("unsigned char[]", length+1)
        buf = ffi.buffer(bufp, length+1)
        buf[0] = report_id
        rv = hidapi.hid_get_feature_report(self._device, bufp, length+1)
        if rv == -1:
            raise IOError("Failed to get feature report from HID device: {0}"
                          .format(self._get_last_error_string()))
        return buf[1:]

    def get_indexed_string(self, idx):
        """ Get a string from the device, based on its string index.

        :param idx: The index of the string to get
        :type idx:  int
        :return:    The string at the index
        :rtype:     unicode

        """
        self._check_device_status()
        bufp = ffi.new("wchar_t*")
        rv = hidapi.hid_get_indexed_string(self._device, idx, bufp, 65536)
        if rv == -1:
            raise IOError("Failed to read string with index {0} from HID "
                          "device: {0}"
                          .format(idx, self._get_last_error_string()))
        return ffi.buffer(bufp, 65536)[:].strip()

    def close(self):
        """ Close connection to HID device.

        Automatically run when a Device object is garbage-collected, though
        manual invocation is recommended.
        """
        self._check_device_status()
        hidapi.hid_close(self._device)
        self._device = None

    def _get_last_error_string(self):
        errstr_p = ffi.new("wchar_t*")
        rv = hidapi.hid_error(self._device)
        if rv is ffi.NULL:
            return None
        return ffi.string(errstr_p)

    def _check_device_status(self):
        if self._device is None:
            raise OSError("Trying to perform action on closed device.")
