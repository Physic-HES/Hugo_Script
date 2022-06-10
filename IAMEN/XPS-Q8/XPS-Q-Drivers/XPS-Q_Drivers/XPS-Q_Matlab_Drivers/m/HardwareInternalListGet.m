function [errorCode, InternalHardwareList] = HardwareInternalListGet(socketId)
%HardwareInternalListGet :  Internal hardware list
%
%	[errorCode, InternalHardwareList] = HardwareInternalListGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		cstring InternalHardwareList


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
InternalHardwareList = '';
for i = 1:103
	InternalHardwareList = [InternalHardwareList '          '];
end

% lib call
[errorCode, InternalHardwareList] = calllib('XPS_Q8_drivers', 'HardwareInternalListGet', socketId, InternalHardwareList);
