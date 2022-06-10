function [errorCode, StartElement, EndElement, TimeInterval] = MultipleAxesPVTPulseOutputGet(socketId, GroupName)
%MultipleAxesPVTPulseOutputGet :  Get pulse output on trajectory configuration
%
%	[errorCode, StartElement, EndElement, TimeInterval] = MultipleAxesPVTPulseOutputGet(socketId, GroupName)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%	* Output parameters :
%		int32 errorCode
%		int32Ptr StartElement
%		int32Ptr EndElement
%		doublePtr TimeInterval


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
StartElement = 0;
EndElement = 0;
TimeInterval = 0;

% lib call
[errorCode, GroupName, StartElement, EndElement, TimeInterval] = calllib('XPS_Q8_drivers', 'MultipleAxesPVTPulseOutputGet', socketId, GroupName, StartElement, EndElement, TimeInterval);
