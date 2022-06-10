function [errorCode] = TZPVTPulseOutputSet(socketId, GroupName, StartElement, EndElement, TimeInterval)
%TZPVTPulseOutputSet :  Configure pulse output on trajectory
%
%	[errorCode] = TZPVTPulseOutputSet(socketId, GroupName, StartElement, EndElement, TimeInterval)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		int32 StartElement
%		int32 EndElement
%		double TimeInterval
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName] = calllib('XPS_C8_drivers', 'TZPVTPulseOutputSet', socketId, GroupName, StartElement, EndElement, TimeInterval);
